# Implementation Checklist

Files are ordered by dependency: implement each file before the ones that import it.

---

## 1. Foundation

- [ ] **`tools/cache.py`** — Define `DATAFRAME_CACHE = {}`. Everything else that touches data imports from here.
- [ ] **`llm/loader.py`** — Implement `load_llm()` returning `ChatOllama(model=..., temperature=0)`. Read model name from `LLM_MODEL` env var, default `"qwen2.5:7b"`.
- [ ] **`agent/state.py`** — Define `AgentState(TypedDict)` with `messages: Annotated[List[BaseMessage], operator.add]` and `dataset_paths: List[str]`.
- [ ] **`agent/prompts.py`** — Write the system prompt string(s) for the ReAct agent (what the LLM should know about available tools and its role).

## 2. Tools

- [ ] **`tools/summary.py`** — Implement tools: `load_dataset(path)` (reads CSV → stores in cache, returns shape/dtypes), `summarize_dataset(name)` (returns describe() + null counts).
- [ ] **`tools/dataframe_ops.py`** — Implement tools: `filter_rows(name, column, value)`, `select_columns(name, columns)`, `show_sample(name, n)`.
- [ ] **`tools/classification.py`** — Implement tool: `run_classification(name, target_column)` (train/test split → LogisticRegression → accuracy, classification report).
- [ ] **`tools/regression.py`** — Implement tool: `run_regression(name, target_column)` (train/test split → LinearRegression → RMSE, R²).
- [ ] **`tools/__init__.py`** — Import all `@tool` functions from the four tool modules; assemble `all_tools: list`.

## 3. Agent Graph

- [ ] **`agent/graph.py`** — Implement `build_graph()`: create `StateGraph(AgentState)`, add `"agent"` node (calls LLM with system prompt), add `"tools"` node (`ToolNode(all_tools)`), wire conditional edge (tool calls → `"tools"`, else `END`), set entry point `"agent"`, compile and return.

## 4. Interface

- [ ] **`interface/app.py`** — Implement `chat(user_message, history)`: convert Gradio history → LangChain messages, call `graph.invoke(...)`, extract and return last message content. Launch `gr.ChatInterface(chat).launch()` under `if __name__ == "__main__"`.

## 5. Docs & Config

- [ ] **`docs/architecture.md`** — Flesh out the graph flow diagram and component table (placeholder exists).
- [ ] **`requirements.txt`** — Pin exact versions after a successful `pip install` smoke test.

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
