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