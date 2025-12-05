from fastapi import APIRouter, HTTPException
from .schemas import MemoryQuery, MemoryResponse, EmptyResponse, MemoryStateResponse
from .memory_graph import get_chat_graph
from .chroma_client import collection
from .utils import get_field
import logging

# ------------------------------------------------------
# Router principal para el módulo A6 Memory
# ------------------------------------------------------
# Define un prefijo "/a6memory" para todos los endpoints,
# facilitando su aislamiento y reconocimiento dentro de la API.
# También agrupa los endpoints bajo la etiqueta "A6 - Memory"
# para documentaciones como Swagger/OpenAPI.
# ------------------------------------------------------
router = APIRouter(prefix="/a6memory", tags=["A6 - Memory (LangGraph)"])


# ======================================================
# POST /a6memory/query
# ------------------------------------------------------
# Punto principal para que el usuario interactúe con el
# sistema de memoria + LangGraph.
#
# Flujo interno:
#   1. Crea un estado inicial con el mensaje del usuario.
#   2. Ejecuta el grafo conversacional (LangGraph).
#   3. El grafo consulta memoria, resume, prepara y llama al LLM.
#   4. Devuelve la respuesta generada + metadatos.
# ======================================================
@router.post(
    "/query",
    summary="Consulta con memoria persistente usando LangGraph",
    description="""
    Implementa un sistema de chat completo que utiliza **LangGraph** para:
    - Mantener el estado conversacional.
    - Preparar y consultar memoria persistente usando ChromaDB.
    - Generar respuestas contextuales con un LLM.
    """,
    response_description="Respuesta generada y detalles de memoria usada",
    response_model=MemoryResponse
)
async def query_memory(req: MemoryQuery):

    # Obtenemos el grafo ya compilado (patrón singleton)
    graph = get_chat_graph()

    # Estado inicial que pasa al grafo
    initial_state = {
        "user_id": req.user_id,
        "messages": [{"role": "user", "content": req.question}],
        "meta": {}
    }

    # ------------------------------------------------------
    # Ejecutar el grafo de forma asíncrona
    # ------------------------------------------------------
    try:
        final_state = await graph.ainvoke(initial_state)
    except Exception as e:
        logging.exception("Graph execution error")
        raise HTTPException(status_code=500, detail=f"Graph execution error: {e}")

    messages = final_state.get("messages", [])

    # ------------------------------------------------------
    # Recuperar la última respuesta del asistente
    # Con fiabilidad: recorriendo desde el final del buffer
    # ------------------------------------------------------
    last_assistant = None
    for m in reversed(messages):
        if get_field(m, "role") == "assistant":
            last_assistant = get_field(m, "content")
            break

    # ------------------------------------------------------
    # Indicar qué tipo de memoria fue usada:
    #  - summary → resumen de mensajes recientes
    #  - buffer  → historial de la conversación
    # ------------------------------------------------------
    memory_used = []
    if final_state.get("summary"):
        memory_used.append("summary")
    if messages:
        memory_used.append("buffer")

    return MemoryResponse(
        answer=last_assistant or "No hay respuesta",
        memory_used=memory_used
    )


# ======================================================
# GET /a6memory/memory_state/{user_id}
# ------------------------------------------------------
# Devuelve todas las memorias almacenadas en ChromaDB para
# el user_id indicado.
#
# Útil para debugging, validación o mostrar memoria al usuario.
# ======================================================
@router.get(
    "/memory_state/{user_id}",
    summary="Recuperar estado de memoria para un usuario",
    description="Recupera los textos de memoria almacenados para un usuario específico.",
    response_model=MemoryStateResponse
)
async def memory_state(user_id: str):
    try:
        results = collection.query(
            query_texts=[""],        # Query vacía → recupera todo lo del usuario
            n_results=100,
            where={"user_id": user_id}
        )
        
        # Los documentos vienen en una lista de listas
        memory_texts = results.get("documents", [[]])[0] 
        
        return {"user_id": user_id, "memory": memory_texts}

    except Exception as e:
        logging.exception("Error retrieving memory")
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {e}")


# ======================================================
# POST /a6memory/clear/{user_id}
# ------------------------------------------------------
# Elimina TODAS las memorias de un usuario.
# Pasos:
#   1. Buscar todos los IDs asociados al user_id.
#   2. Eliminar esos IDs en ChromaDB.
#
# Ideal para pruebas o reiniciar el estado de un usuario.
# ======================================================
@router.post(
    "/clear/{user_id}",
    summary="Borrar memoria para un usuario",
    description="Elimina todas las entradas de memoria asociadas a un usuario específico.",
    response_model=EmptyResponse
)
async def clear_memory(user_id: str):
    try:
        # Recuperar todas las memorias con sus IDs
        results = collection.query(
            query_texts=[""],
            n_results=1000,
            where={"user_id": user_id}
        )

        ids_to_delete = results["ids"][0] if results and "ids" in results else []

        # Si existen, eliminar de ChromaDB
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)

        return EmptyResponse(ok=True)

    except Exception as e:
        logging.exception("Error clearing memory")
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {e}")
