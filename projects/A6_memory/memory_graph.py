from langgraph.graph import StateGraph, START, END
from .llm_node import call_llm_node

# Nodo: Añadir mensaje del usuario al estado
async def add_user_message_node(state: dict) -> dict:
    state.setdefault("messages", [])
    # Ya asumimos que el mensaje del usuario se pasa en state["messages"]
    return state

# Construir grafo
_COMPILED_CHAT_GRAPH = None

def build_chat_graph():
    graph = StateGraph(dict)
    graph.add_node("add_user_message", add_user_message_node)
    graph.add_node("call_llm", call_llm_node)

    graph.add_edge(START, "add_user_message")
    graph.add_edge("add_user_message", "call_llm")
    graph.add_edge("call_llm", END)

    return graph.compile()

def get_chat_graph():
    global _COMPILED_CHAT_GRAPH
    if _COMPILED_CHAT_GRAPH is None:
        _COMPILED_CHAT_GRAPH = build_chat_graph()
    return _COMPILED_CHAT_GRAPH
