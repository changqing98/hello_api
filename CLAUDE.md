# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`owesome_agent` is an educational agent framework accompanying the "Hello Agents" book. It implements core AI agent paradigms (ReAct, etc.) in Python using an OpenAI-compatible LLM client.

## Running Code

Each module in `paradigm/` has a standalone `__main__` block for testing:

```bash
python paradigm/llm_client.py   # test LLM client
python paradigm/search.py       # test search tool + ToolExecutor
```

## Environment Setup

Copy `.env` and fill in values before running anything:

```
LLM_API_KEY=...
LLM_MODEL_ID=...
LLM_BASE_URL=...      # any OpenAI-compatible endpoint
SERPAPI_API_KEY=...   # required for Search tool
```

## Architecture

The three files in `paradigm/` form a layered stack:

- **`llm_client.py`** — `HelloAgentsLLM`: thin wrapper around the OpenAI SDK. Uses streaming by default. Reads config from `.env` but accepts constructor overrides. The `think(messages)` method is the single entry point for all LLM calls.

- **`react.py`** — `REACT_PROMPT_TEMPLATE`: the ReAct prompt skeleton. Expects `{tools}`, `{question}`, and `{history}` placeholders to be filled at runtime. Drives the Thought → Action → Observation loop.

- **`search.py`** — `ToolExecutor` + `search()`: `ToolExecutor` is a tool registry (register/get/list). The `search()` function is a SerpApi-backed Google search that prioritizes answer boxes and knowledge graphs before falling back to organic snippets.

New agent paradigms should follow this pattern: add a prompt template, implement tool functions, wire them through `ToolExecutor`, and use `HelloAgentsLLM.think()` to drive the loop.
