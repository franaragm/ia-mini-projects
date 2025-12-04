from langgraph.graph import StateGraph, START, END
from .llm_node import call_llm_node


async def add_user_message_node(state: dict) -> dict:
    state.setdefault("messages", [])
    return state


async def maybe_summarize_node(state: dict) -> dict:
    messages = state.get("messages", [])
    state["summary"] = "\n".join([f"{m['role']}: {m['content']}" for m in messages[-10:]])
    return state


_COMPILED_CHAT_GRAPH = None


def build_chat_graph():
    graph = StateGraph(dict)
    graph.add_node("add_user_message", add_user_message_node)
    graph.add_node("maybe_summarize", maybe_summarize_node)
    graph.add_node("call_llm", call_llm_node)

    graph.add_edge(START, "add_user_message")
    graph.add_edge("add_user_message", "maybe_summarize")
    graph.add_edge("maybe_summarize", "call_llm")
    graph.add_edge("call_llm", END)

    return graph.compile()


def get_chat_graph():
    global _COMPILED_CHAT_GRAPH
    if _COMPILED_CHAT_GRAPH is None:
        _COMPILED_CHAT_GRAPH = build_chat_graph()
    return _COMPILED_CHAT_GRAPH
