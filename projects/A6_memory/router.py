from fastapi import APIRouter, HTTPException
from .schemas import MemoryQuery, MemoryResponse, EmptyResponse, MemoryStateResponse
from .memory_graph import get_chat_graph
from .chroma_client import collection
import logging

router = APIRouter(prefix="/memory", tags=["Memory Simple"])

@router.post("/query", response_model=MemoryResponse)
async def query_memory(req: MemoryQuery):
    graph = get_chat_graph()

    initial_state = {
        "user_id": req.user_id,
        "messages": [{"role": "user", "content": req.question}]
    }

    try:
        final_state = await graph.ainvoke(initial_state)
    except Exception as e:
        logging.exception("Graph execution error")
        raise HTTPException(status_code=500, detail=f"Graph execution error: {e}")

    messages = final_state.get("messages", [])
    last_assistant = next(
        (m["content"] for m in reversed(messages) if m["role"] == "assistant"),
        "No hay respuesta"
    )

    # eliminamos guardado duplicado aquí
    return MemoryResponse(answer=last_assistant, memory_used=messages)


@router.get("/state/{user_id}", response_model=MemoryStateResponse)
async def memory_state(user_id: str):
    try:
        results = collection.query(
            query_texts=[""],
            n_results=200,
            where={"user_id": user_id}
        )
        memory_texts = results.get("documents", [[]])[0]
        return {"user_id": user_id, "memory": memory_texts}
    except Exception as e:
        logging.exception("Error retrieving memory")
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {e}")


@router.post("/clear/{user_id}", response_model=EmptyResponse)
async def clear_memory(user_id: str):
    try:
        results = collection.query(
            query_texts=[""],
            n_results=2000,
            where={"user_id": user_id}
        )
        ids_to_delete = results.get("ids", [[]])[0]
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
        return EmptyResponse(ok=True)
    except Exception as e:
        logging.exception("Error clearing memory")
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {e}")
