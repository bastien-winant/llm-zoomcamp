from rag_helper import RAGTraced

from dotenv import load_dotenv
from openai import OpenAI

from ingest import load_github_data, build_index

import sys


def create_assistant():
	load_dotenv(override=True)
	
	documents = load_github_data()
	index = build_index(documents)

	return RAGTraced(index=index, llm_client=OpenAI())


if __name__ == "__main__":
	assistant = create_assistant()
	query = "How does the agentic loop keep calling the model until it stops?"
	if len(sys.argv) > 1:
		query = sys.argv[1]

	answer = assistant.traced_rag(query)
	print(answer)