"""Gradio ChatInterface entry point."""

import gradio as gr
from langchain_core.messages import AIMessage, HumanMessage

from agent.graph import build_graph

# Build once at module load — not inside chat() — to avoid reconnecting on every message
graph = build_graph()


def chat(user_message: str, history: list) -> str:
    # Gradio 4.x history format: list of {"role": "user"|"assistant", "content": str}
    lc_messages = []
    for turn in history:
        if turn["role"] == "user":
            lc_messages.append(HumanMessage(content=turn["content"]))
        elif turn["role"] == "assistant":
            lc_messages.append(AIMessage(content=turn["content"]))
    lc_messages.append(HumanMessage(content=user_message))

    result = graph.invoke({"messages": lc_messages, "dataset_paths": []})
    return result["messages"][-1].content


if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat,
        title="Data Analysis Agent",
        description="Ask me to analyze CSV datasets.",
        type="messages",  # opt into Gradio 4.x dict-based history
    ).launch()
