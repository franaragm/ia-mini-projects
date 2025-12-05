from langgraph.graph import StateGraph, START, END
from .llm_node import call_llm_node


# ======================================================
# Nodo 1: add_user_message_node
# ------------------------------------------------------
# Este nodo no modifica realmente el estado, solo garantiza
# que exista una lista "messages" donde el grafo guardará
# los mensajes del usuario antes de continuar el flujo.
# Es un nodo muy simple pero obligatorio para mantener
# la estructura del estado coherente.
# ======================================================
async def add_user_message_node(state: dict) -> dict:
    state.setdefault("messages", [])
    return state


# ======================================================
# Nodo 2: maybe_summarize_node
# ------------------------------------------------------
# Este nodo crea un pequeño resumen de los últimos mensajes.
# El objetivo es mantener un "mini contexto" accesible para
# otros nodos del grafo (por ejemplo para logging o análisis).
#
# Este resumen NO se guarda en ChromaDB.
# Solo sirve como campo auxiliar dentro del estado del grafo.
# ======================================================
async def maybe_summarize_node(state: dict) -> dict:
    messages = state.get("messages", [])
    
    # Creamos un resumen concatenando los últimos 10 mensajes
    # en formato: "role: contenido".
    state["summary"] = "\n".join([
        f"{m['role']}: {m['content']}" 
        for m in messages[-10:]
    ])
    
    return state


# Variable global donde se guarda el grafo compilado
_COMPILED_CHAT_GRAPH = None


# ======================================================
# Función: build_chat_graph
# ------------------------------------------------------
# Crea el grafo conversacional completo de LangGraph.
# La estructura del grafo es:
#
# START → add_user_message
#         → maybe_summarize
#         → call_llm
#         → END
#
# El grafo se devuelve compilado para ser utilizado por
# el router en cada llamada /query.
# ======================================================
def build_chat_graph():
    # El estado base del grafo es un dict
    graph = StateGraph(dict)

    # Añadimos los nodos del flujo
    graph.add_node("add_user_message", add_user_message_node)
    graph.add_node("maybe_summarize", maybe_summarize_node)
    graph.add_node("call_llm", call_llm_node)

    # Definimos transiciones entre nodos
    graph.add_edge(START, "add_user_message")
    graph.add_edge("add_user_message", "maybe_summarize")
    graph.add_edge("maybe_summarize", "call_llm")
    graph.add_edge("call_llm", END)

    # Compilamos el grafo para ejecución
    return graph.compile()


# ======================================================
# Función: get_chat_graph
# ------------------------------------------------------
# Devuelve el grafo ya compilado.
# Se crea solo una vez (patrón singleton) para ahorrar
# tiempo y evitar compilar el grafo múltiples veces.
# ======================================================
def get_chat_graph():
    global _COMPILED_CHAT_GRAPH
    
    # Si aún no existe, se construye
    if _COMPILED_CHAT_GRAPH is None:
        _COMPILED_CHAT_GRAPH = build_chat_graph()
    
    # Siempre devuelve el grafo ya compilado
    return _COMPILED_CHAT_GRAPH
