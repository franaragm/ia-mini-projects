from fastapi import APIRouter, HTTPException
from .schemas import MemoryQuery, MemoryResponse, EmptyResponse
from .memory_graph import get_chat_graph
from .chroma_client import collection
import logging

router = APIRouter(prefix="/a6memory", tags=["A6 - Memory (LangGraph)"])


def get_field(obj, key):
    """Extrae atributo seguro desde dict o Pydantic."""
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


@router.post("/query", response_model=MemoryResponse)
async def query_memory(req: MemoryQuery):

    graph = get_chat_graph()
    initial_state = {
        "user_id": req.user_id,
        "messages": [{"role": "user", "content": req.question}],
        "meta": {}
    }

    try:
        final_state = await graph.ainvoke(initial_state)
    except Exception as e:
        logging.exception("Graph execution error")
        raise HTTPException(status_code=500, detail=f"Graph execution error: {e}")

    messages = final_state.get("messages", [])

    # -----------------------------
    # Extraer última respuesta robusta
    # -----------------------------
    last_assistant = None
    for m in reversed(messages):
        if get_field(m, "role") == "assistant":
            last_assistant = get_field(m, "content")
            break

    memory_used = []
    if final_state.get("summary"):
        memory_used.append("summary")
    if messages:
        memory_used.append("buffer")

    return MemoryResponse(
        answer=last_assistant or "No hay respuesta",
        memory_used=memory_used
    )


@router.get("/memory_state/{user_id}")
async def memory_state(user_id: str):
    try:
        results = collection.query(
            query_texts=[""],
            n_results=100,
            where={"user_id": user_id}
        )
        memory_texts = results["documents"][0] if results and "documents" in results else []
        return {"user_id": user_id, "memory": memory_texts}
    except Exception as e:
        logging.exception("Error retrieving memory")
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {e}")


@router.post("/clear/{user_id}")
async def clear_memory(user_id: str):
    try:
        results = collection.query(
            query_texts=[""],
            n_results=1000,
            where={"user_id": user_id}
        )
        ids_to_delete = results["ids"][0] if results and "ids" in results else []

        if ids_to_delete:
            collection.delete(ids=ids_to_delete)

        return EmptyResponse(ok=True)
    except Exception as e:
        logging.exception("Error clearing memory")
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {e}")
