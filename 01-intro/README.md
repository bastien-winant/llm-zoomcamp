# Module 1: Introduction
## Motivating problem
__Problem:__ Bloated documentation makes it hard for users to find relevant information
__Solution:__ Build a Q&A bot that can answer questions based on the content of the documentation

## Large-Language Models
Language models use artificial intelligence techniques to *predict* the next word in a sequence.
Many of us make daily use of such models when we let our phones auto-complete our texts.

Large Language Model (LLM) have many parameters (usually billions) that allow them to extrapolate predictions
and mimic human conversations. They are capable of synthesizing large pieces of text, and produce meaningful responses.
The inputs given to LLMs are commonly referred to as __prompts__.

## Retrieval-Augmented Generation
We often want LLMs to do more than act as digital conversationalists. In order to provide useful and accurate
information on a particular topic, the model needs to access a knowledge base and be able to work it into its responses.

The knowledge base that the model will retrieve from can take many forms, and have substantial impact on the quality of
the outputs produced by an LLM.
