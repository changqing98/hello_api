# owesome_agent

A hands-on implementation of the **ReAct** (Reasoning + Acting) agent paradigm, built as a companion to the book *Hello Agents*.

## Overview

This project demonstrates how to build an LLM-powered agent that can reason step-by-step and call external tools to answer questions it cannot solve from memory alone.

```
Thought → Action (tool call or Finish) → Observation → Thought → ...
```

## Project Structure

```
paradigm/
├── llm_client.py   # OpenAI-compatible LLM client with streaming
├── react.py        # ReAct prompt template
└── search.py       # SerpApi web search tool + ToolExecutor registry
```

### Key Components

| Module | Class / Function | Purpose |
|--------|-----------------|---------|
| `llm_client.py` | `HelloAgentsLLM` | Wraps any OpenAI-compatible API; streams responses |
| `search.py` | `ToolExecutor` | Register, retrieve, and describe tools |
| `search.py` | `search()` | Live web search via SerpApi (Google engine) |
| `react.py` | `REACT_PROMPT_TEMPLATE` | Prompt template that drives the ReAct loop |

## Setup

### 1. Install dependencies

```bash
pip install openai python-dotenv google-search-results
```

### 2. Configure environment

Copy the template and fill in your keys:

```bash
cp .env.example .env   # or create .env manually
```

Required variables in `.env`:

```env
LLM_API_KEY=<your-api-key>
LLM_MODEL_ID=<model-id>
LLM_BASE_URL=<openai-compatible-base-url>
SERPAPI_API_KEY=<your-serpapi-key>
```

> `LLM_TIMEOUT` is optional (default: 60 seconds).

### 3. Run the examples

```bash
# Test the LLM client
python paradigm/llm_client.py

# Test the search tool
python paradigm/search.py
```

## How It Works

1. **`HelloAgentsLLM.think(messages)`** sends a message list to the configured LLM and returns the full response text (streamed to stdout in real time).

2. **`ToolExecutor`** holds a registry of named tools. Each tool has a description (surfaced to the LLM) and a callable implementation.

3. **`REACT_PROMPT_TEMPLATE`** injects the available tool descriptions and the conversation history into a prompt that instructs the model to emit `Thought:` / `Action:` pairs until it reaches `Finish[answer]`.

4. The agent loop (to be wired in the caller) parses the model's `Action:` field, dispatches to the matching tool, feeds the `Observation` back into the history, and repeats until `Finish`.

## License

MIT
