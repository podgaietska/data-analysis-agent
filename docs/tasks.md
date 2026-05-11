# Implementation Checklist

Files are ordered by dependency: implement each file before the ones that import it.

---

## 1. Foundation

- [x] **`tools/cache.py`** — Define `DATAFRAME_CACHE = {}`. Everything else that touches data imports from here.
- [x] **`llm/loader.py`** — Implement `load_llm()` returning `ChatOllama(model=..., temperature=0)`. Read model name from `LLM_MODEL` env var, default `"qwen2.5:7b"`.
- [x] **`agent/state.py`** — Define `AgentState(TypedDict)` with `messages: Annotated[List[BaseMessage], operator.add]` and `dataset_paths: List[str]`.
- [x] **`agent/prompts.py`** — Write the system prompt string(s) for the ReAct agent (what the LLM should know about available tools and its role).

## 2. Tools

- [x] **`tools/summary.py`** — `preload_datasets`, `get_dataset_summaries`.
- [x] **`tools/dataframe_ops.py`** — `call_dataframe_method`.
- [x] **`tools/classification.py`** — `evaluate_classification_dataset` (RandomForestClassifier → accuracy).
- [x] **`tools/regression.py`** — `evaluate_regression_dataset` (RandomForestRegressor → R², MSE).
- [x] **`tools/__init__.py`** — Import all `@tool` functions from the four tool modules; assemble `all_tools: list`.

## 3. Agent Graph

- [x] **`agent/graph.py`** — Implement `build_graph()`: create `StateGraph(AgentState)`, add `"agent"` node (calls LLM with system prompt), add `"tools"` node (`ToolNode(all_tools)`), wire conditional edge (tool calls → `"tools"`, else `END`), set entry point `"agent"`, compile and return.

## 4. Interface

- [x] **`interface/app.py`** — Implement `chat(user_message, history)`: convert Gradio history → LangChain messages, call `graph.invoke(...)`, extract and return last message content. Launch `gr.ChatInterface(chat).launch()` under `if __name__ == "__main__"`.

## 5. Docs & Config

- [ ] **`docs/architecture.md`** — Flesh out the graph flow diagram and component table (placeholder exists).
- [ ] **`requirements.txt`** — Pin exact versions after a successful `pip install` smoke test.
- [x] **`.env.example`** — Document `LLM_MODEL` env var with default value.

---

## Smoke Tests (run after each section)

```bash
# After section 1
python -c "from tools.cache import DATAFRAME_CACHE; from llm.loader import load_llm; print('foundation OK')"

# After section 2
python -c "from tools import all_tools; print(len(all_tools), 'tools registered')"

# After section 3
python -c "from agent.graph import build_graph; g = build_graph(); print('graph OK')"

# After section 4
python -m interface.app  # should open Gradio UI at localhost:7860
```
