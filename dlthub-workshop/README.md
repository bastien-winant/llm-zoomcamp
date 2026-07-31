# Data Ingestion
## AI agent traces
AI agents produce a lot of logs, known as _agent traces_, as the system makes decisions and takes action.
This session data is usually stored in local files and holds information such as token usage or potential secret leakages.

An agent will be able to answer ad-hoc questions from the raw files. For a more systematic analysis, we may want to build a shareable dashboard that provides a clear overview of agent metrics.
For this purpose, we require a pipeline that pulls trace data from an accessible source and loads it into a data store on top of which to build reports.

## Loggers and telemetry
A logger can be used to track how an agent behaves in production
- token usage
- model
- tool calls
- skills used

This metadata can be analyzd to understand and optimize the agent.

Many logger tools are available that store agent metadata in the cloud, and make it available via an API.
In our agent dashboard scenario, this API constitutes the raw data source for the pipeline.
