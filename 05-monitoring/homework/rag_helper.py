from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, SpanExporter, SpanExportResult
import sqlite3

from metrics import calculate_cost

class SQLiteSpanExporter(SpanExporter):
	def __init__(self, db_path="traces.db"):
		self.conn = sqlite3.connect(db_path)
		self.conn.execute("""
			CREATE TABLE IF NOT EXISTS spans (
					name TEXT,
					start_time INTEGER,
					end_time INTEGER,
					input_tokens INTEGER,
					output_tokens INTEGER,
					cost REAL
			)
		""")
		self.conn.commit()

	def export(self, spans):
		for span in spans:
			attrs = dict(span.attributes or {})
			self.conn.execute(
				"INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
				(
					span.name,
					span.start_time,
					span.end_time,
					attrs.get("input_tokens"),
					attrs.get("output_tokens"),
					attrs.get("cost"),
				),
			)
		self.conn.commit()
		return SpanExportResult.SUCCESS

	def shutdown(self):
		self.conn.close()

	def force_flush(self):
		return True


INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


class RAGBase:
	def __init__(
		self,
		index,
		llm_client,
		instructions=INSTRUCTIONS,
		prompt_template=PROMPT_TEMPLATE,
		model='gpt-5.4-mini'
	):
		self.index = index
		self.llm_client = llm_client
		self.instructions = instructions
		self.prompt_template = prompt_template
		self.model = model

	def search(self, query, num_results=5):
		return self.index.search(query, num_results=num_results)

	def build_context(self, search_results):
		lines = []

		for doc in search_results:
			lines.append(doc['filename'])
			lines.append(doc['content'])
			lines.append('')

		return '\n'.join(lines).strip()

	def build_prompt(self, query, search_results):
		context = self.build_context(search_results)
		return self.prompt_template.format(
			question=query, context=context
		)

	def llm(self, prompt):
		input_messages = [
			{'role': 'developer', 'content': self.instructions},
			{'role': 'user', 'content': prompt}
		]

		response = self.llm_client.responses.create(
			model=self.model,
			input=input_messages
		)

		return response

	def rag(self, query):
		search_results = self.search(query)
		prompt = self.build_prompt(query, search_results)
		response = self.llm(prompt)
		return response.output_text


class RAGTraced(RAGBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		provider = TracerProvider()
		provider.add_span_processor(
			SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
		)
		trace.set_tracer_provider(provider)

		self.tracer = trace.get_tracer("llm-zoomcamp")

	def traced_search(self, query, num_results=5):
		with self.tracer.start_as_current_span("search") as span:
			return self.search(query=query, num_results=num_results)

	def traced_llm(self, prompt):
		with self.tracer.start_as_current_span("llm") as span:
			response = self.llm(prompt=prompt)
			usage = response.usage

			span.set_attribute("input_tokens", usage.input_tokens)
			span.set_attribute("output_tokens", usage.output_tokens)
			span.set_attribute("cost", calculate_cost(usage=usage))

			return response

	def traced_rag(self, query):
		with self.tracer.start_as_current_span("rag") as span:
			search_results = self.traced_search(query)
			prompt = self.build_prompt(query, search_results)
			response = self.traced_llm(prompt)
			return response.output_text