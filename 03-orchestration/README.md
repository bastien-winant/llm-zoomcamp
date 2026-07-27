## Using AI in workflows
### Generating worflows with AI
Building LLM applications usually involves a lot of repeated boilerplate code. This is where an AI assistant can be helpful and speed up development.

AI also helps avoid errors, correct syntax errors, and ensure best coding practices. LLM-assisted coding often involves a process of refinement where the developer looks over the AI-generated code, spots potential mistakes or gaps, and crafts a new prompt asking the model to address the issues.

The _5% rule_ refers to the notion that AI models, if prompted adequately, are generally able to generate 95% of a feature's code. The developer then fills the gaps appropriately to complete the program and achieve the desired functionality.

### Automating decisions with AI
Inside a workflow, AI can automate complex decisions. Given some input data, AI's non-determinism allows it to adapt to the specificities of the provided context.

Using RAG, we can ground AI responses in data and ensure the model step of our workflow provides accurate information.

But AI is usually only as useful as the context it is provided. Context engineering is the practice of providing enough background information for an LLM to generate accurate and complete outputs, while minimizing irrelevant information that may cause confusion and hallucinations on the part of the model.

LLM models are only trained up to a certain point in time. Eventually, their built-in knowledge becomes out-of-date and potentially obsolete. This knowledge gap is usually bridged using a carefully cured context. Therefore, proper context engineering becomes key in ensuring the reliability of AI applications and maintaining trust.

### Separating ingestion from querying in RAG
At a high level, RAG is a technique for retrieving relevant information from an external data source, and passing it to an AI model to elicit grounded responses. This helps in solving the hallucination problem often encountered with AI by ensuring the model has access to accurate data at query time.

RAG has 2 phases:
1. an _ingestion_ stage on a cadence
2. on demand _querying_

In productionl, theses 2 phases are executed separately and independently. Scheduled data ingestion ensures that retrieval returns up-to-date information. In turn, the amount of data processing at query time is minimized.

During ingestion, new documents are collected, embedded into numerical vectors, and saved in a data store. At query time, a search engine uses a vector algorithm to identify documents from the database that closely match the query to build a prompt context.

### Tools in RAG
As a secondary method for improving LLM model responses, we can provide AI with tools that may be called upon to improve model responses. Most commonly, a _web search tool_ allows the LLM to perform a web search for additional information related to the user query.

Tools are often easier to set up than a data ingestion/retrieval process, but will generally not have the same level of reliability.

### Agentic workflows