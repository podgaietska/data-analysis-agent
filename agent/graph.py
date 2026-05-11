"""LangGraph graph definition; exposes build_graph()."""

from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from agent.prompts import SYSTEM_PROMPT
from agent.state import AgentState
from llm.loader import load_llm
from tools import all_tools


def build_graph():
    llm = load_llm()
    llm_with_tools = llm.bind_tools(all_tools)

    def agent_node(state: AgentState) -> dict:
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
        ai_message = llm_with_tools.invoke(messages)
        return {"messages": [ai_message]}

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(all_tools))

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END
        },
    )
    graph.add_edge("tools", "agent")

    return graph.compile()
