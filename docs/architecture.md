# Architecture

> Placeholder — fill in after all modules are implemented.

## Graph Flow

```
[User message]
      │
      ▼
  agent node  ──── no tool calls ────▶ END
      │
  tool calls?
      │
      ▼
  tools node
      │
      └──────────────────────────────▶ agent node (loop)
```

## Key Components

| Component | File | Role |
|-----------|------|------|
| State | `agent/state.py` | Shared `AgentState` TypedDict |
| Prompts | `agent/prompts.py` | System prompt for ReAct agent |
| Graph | `agent/graph.py` | Builds and returns compiled LangGraph |
| LLM | `llm/loader.py` | Wraps `ChatOllama` |
| Cache | `tools/cache.py` | `DATAFRAME_CACHE` shared dict |
| Tools | `tools/*.py` | `@tool` functions bound to LLM |
| Interface | `interface/app.py` | Gradio `ChatInterface` |
