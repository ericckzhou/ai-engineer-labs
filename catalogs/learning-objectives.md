# Learning Objectives

All learning objectives across the curriculum. Used for:
- Progress tracking in `memory/learner/skill-map.md`
- Assessment design in `evaluations/`
- Curriculum coherence checking

---

## Status Key

- `[ ]` Not started
- `[~]` In progress
- `[x]` Demonstrated (passed rubric)
- `[!]` Known difficulty — see misconceptions

---

## Project 1: AI Chatbot

- `[ ]` Call a chat completion API and understand every field in request/response
- `[ ]` Implement multi-turn conversation with correct message history
- `[ ]` Explain why context windows exist and what happens at the limit
- `[ ]` Stream tokens to the UI in real time
- `[ ]` Calculate cost per API call and project costs at scale
- `[ ]` Design system prompts that reliably change model behavior
- `[ ]` Switch providers via LiteLLM without changing application logic
- `[ ]` Identify when a chatbot is the right architecture

## Project 2: Token & Embedding Explorer

- `[ ]` Explain what a token is and why LLMs use them
- `[ ]` Predict token count before calling the API
- `[ ]` Explain what an embedding vector is
- `[ ]` Calculate cosine similarity by hand
- `[ ]` Explain why embedding arithmetic (king - man + woman ≈ queen) works
- `[ ]` Choose the right embedding model for a task
- `[ ]` Identify semantic similarity across different surface forms
- `[ ]` Distinguish tokenizer from embedding model

## Project 3: Semantic Search

- `[ ]` Build an embedding pipeline over a corpus
- `[ ]` Store and query vectors in ChromaDB
- `[ ]` Implement and explain cosine similarity retrieval
- `[ ]` Compare semantic vs. keyword search on concrete failure cases
- `[ ]` Design and evaluate a hybrid search strategy
- `[ ]` Explain indexing vs. query performance tradeoffs
- `[ ]` Identify the top 5 failure modes of semantic search

## Project 4: PDF Research Assistant (RAG)

- `[ ]` Implement the full RAG pipeline end-to-end
- `[ ]` Design and compare chunking strategies
- `[ ]` Detect hallucination via faithfulness checking
- `[ ]` Build a citation system linking answers to source passages
- `[ ]` Evaluate RAG quality with RAGAS-style metrics
- `[ ]` Name and explain the 5 failure modes of RAG

## Project 5: Personal Memory System

- `[ ]` Implement episodic, semantic, and procedural memory storage
- `[ ]` Design memory retrieval with recency and relevance scoring
- `[ ]` Implement memory decay and explain why it exists
- `[ ]` Handle memory conflicts
- `[ ]` Evaluate memory retrieval quality quantitatively
- `[ ]` Address privacy concerns in memory design

## Project 6: AI Coding Copilot

- `[ ]` Implement tool use with file system and search tools
- `[ ]` Build context selection that injects the right files
- `[ ]` Design system prompts for consistent code output
- `[ ]` Implement code understanding via retrieval
- `[ ]` Evaluate copilot quality: correctness, relevance, hallucination rate

## Project 7: AI Evaluation Framework

- `[ ]` Design evaluation datasets (good vs. bad test cases)
- `[ ]` Implement LLM-as-judge and explain its biases
- `[ ]` Build faithfulness, relevance, and correctness metrics
- `[ ]` Write regression tests that catch prompt degradation
- `[ ]` Track cost, latency, and token usage per eval run
- `[ ]` Interpret eval results and make engineering decisions from them

## Project 8: AI Agent

- `[ ]` Implement the ReAct agent loop
- `[ ]` Build and register custom tools with schemas
- `[ ]` Handle tool errors and implement recovery strategies
- `[ ]` Implement structured output for agent final responses
- `[ ]` Detect and break agent loops
- `[ ]` Evaluate agent performance: task completion, efficiency, cost
- `[ ]` Define when an agent is overkill

## Project 9: Personal Learning OS

- `[ ]` Design a multi-component AI system with clear interfaces
- `[ ]` Integrate memory, retrieval, agents, and evaluation
- `[ ]` Design for extensibility
- `[ ]` Define a personal knowledge graph data model
- `[ ]` Implement query routing across components
- `[ ]` Evaluate the system holistically
- `[ ]` Apply build vs. buy lens to a full system architecture

---

## Cross-Cutting Skills (emerge across multiple projects)

- `[ ]` Evaluate AI systems quantitatively (not impressionistically)
- `[ ]` Apply the build vs. buy framework to every major decision
- `[ ]` Identify production failure modes before they occur
- `[ ]` Read and cite primary sources (papers, official docs)
- `[ ]` Write clear engineering decision records
- `[ ]` Connect AI engineering patterns to StarcallOS architecture
