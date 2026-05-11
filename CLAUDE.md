# CLAUDE.md
 
## What This Project Is
 
A LangGraph-based agentic system that lets users analyze CSV datasets through a
Gradio chat interface. The agent uses a local LLM (via Ollama) and a toolkit of
data analysis tools to load, summarize, and run ML evaluations on datasets.
 
## Repo Layout
 
```
data-analysis-agent/
├── agent/          # LangGraph graph, state, prompts
├── tools/          # All @tool functions + shared DATAFRAME_CACHE
├── llm/            # LLM loader (Ollama by default)
├── interface/      # Gradio chat app
├── data/           # Drop CSV datasets here
├── docs/           # Architecture notes, task checklists
└── notebooks/      # Scratch exploration
```
 
## Stack
 
- **LangGraph** — agent graph (ReAct loop: agent node → ToolNode → agent node)
- **LangChain** — tool definitions (`@tool`), message types, LLM binding
- **Ollama** — local LLM server (default model: `qwen2.5:7b`)
- **Gradio** — chat UI (`gr.ChatInterface`)
- **pandas / scikit-learn** — data analysis and ML evaluation tools
## Key Architectural Rules
 
### DATAFRAME_CACHE
 
- Lives in `tools/cache.py` as a single module-level dict: `DATAFRAME_CACHE = {}`
- ALL tool modules import it from there: `from tools.cache import DATAFRAME_CACHE`
- Never redefine it in another module — one source of truth
### Tools
 
- All tools are decorated with `@tool` from `langchain_core.tools`
- All tools are registered in `tools/__init__.py` as `all_tools: list`
- The graph binds tools to the LLM via `llm.bind_tools(all_tools)`
- Tool files: `cache.py`, `summary.py`, `dataframe_ops.py`, `classification.py`, `regression.py`
### Agent Graph (`agent/graph.py`)
 
- Two nodes: `"agent"` (calls LLM) and `"tools"` (LangGraph `ToolNode`)
- Conditional edge: if last message has `.tool_calls` → route to `"tools"`, else END
- Entry point: `"agent"`
- Returns compiled graph from `build_graph()`
### State (`agent/state.py`)
 
- `AgentState` is a `TypedDict` with:
  - `messages: Annotated[List[BaseMessage], operator.add]`
  - `dataset_paths: List[str]`
### LLM Loader (`llm/loader.py`)
 
- Returns a `ChatOllama` instance (temperature=0 for deterministic tool use)
- Model name configurable via `LLM_MODEL` env var, default `"qwen2.5:7b"`
- Ollama must be running locally on port 11434
### Gradio Interface (`interface/app.py`)
 
- Uses `gr.ChatInterface` with a `chat(user_message, history)` function
- Converts Gradio history tuples → LangChain `HumanMessage`/`AIMessage` list
- Invokes `graph.invoke({"messages": ..., "dataset_paths": []})` each turn
- Extracts reply from `result["messages"][-1].content`
## Commands
 
```bash
# Install deps
pip install -r requirements.txt
 
# Start Ollama (separate terminal)
ollama serve
ollama pull qwen2.5:7b
 
# Run the app
python -m interface.app
 
# Smoke test
python -c "from agent.graph import build_graph; g = build_graph(); print('OK')"
```
 
## Do NOT
 
- Do not put `DATAFRAME_CACHE = {}` anywhere except `tools/cache.py`
- Do not use `from langchain.tools import tool` — use `from langchain_core.tools import tool`
- Do not add state-saving logic to the Gradio chat function (graph is stateless per turn)
- Do not hardcode the model name — read from env or use the default constant in `llm/loader.py`
## Reference Docs
 
- `@docs/architecture.md` — detailed graph flow diagram (create this early)
- `@docs/tasks.md` — implementation checklist with [ ] checkboxes

## Notes

- License: Apache 2.0
- Update this file as the project structure, tooling, and commands are established.
