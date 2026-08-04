from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from rag_helper import RAGBase

provider = TracerProvider()
provider.add_span_processor(
	SimpleSpanProcessor(ConsoleSpanExporter())
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")


class RAGTraced(RAGBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def traced_search(self, query, num_results=5):
		with tracer.start_as_current_span("search") as span:
			self.search(query=query, num_results=num_results)

	def traced_llm(self, prompt):
		with tracer.start_as_current_span("llm") as span:
			self.llm(prompt=prompt)

	def traced_rag(self, query):
		with tracer.start_as_current_span("rag") as span:
			self.rag(query=query)