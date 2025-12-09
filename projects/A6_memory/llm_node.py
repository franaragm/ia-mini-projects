from typing import Dict, Any, List
from app.services.llm_client import llm
from .prompts import memory_preparation_prompt, memory_prompt
from .utils import clean_memory_text, normalize_text
from .chroma_client import collection
import uuid
import logging

SEMANTIC_DUPLICATE_THRESHOLD = 0.87  # umbral de similitud


async def memory_exists(user_id: str, memory: str) -> bool:
    """Detecta duplicado semántico real en Chroma."""
    try:
        q = collection.query(
            query_texts=[memory],
            n_results=3,
            where={"user_id": user_id}
        )
        distances = q.get("distances", [[]])[0]
        if distances:
            return min(distances) < (1 - SEMANTIC_DUPLICATE_THRESHOLD)
    except:
        logging.exception("Error checking duplicates")
    return False


async def call_llm_node(state: Dict[str, Any]) -> Dict[str, Any]:
    user_id = state.get("user_id")
    messages = state.get("messages", [])

    # =============================
    # 1. PROCESAR Y GUARDAR MEMORIA NUEVA
    # =============================
    if user_id:
        for m in messages:
            if m["role"] != "user":
                continue

            try:
                prep_prompt = memory_preparation_prompt.format(input=m["content"])
                prepared = await llm(prep_prompt)

                prepared = clean_memory_text(prepared)
                if not prepared:
                    continue

                normalized = normalize_text(prepared)

                # **NO GUARDAR SI YA EXISTE**
                if await memory_exists(user_id, normalized):
                    continue

                # Guardar memoria nueva
                collection.add(
                    documents=[normalized],
                    metadatas=[{"user_id": user_id}],
                    ids=[f"{user_id}_{uuid.uuid4().hex}"]
                )
            except Exception as e:
                logging.exception("Error preparando memoria: %s", e)

    # =============================
    # 2. Recuperar memoria
    # =============================
    memory_docs = []
    if user_id:
        try:
            results = collection.query(
                query_texts=[""],
                n_results=100,
                where={"user_id": user_id}
            )
            memory_docs = results.get("documents", [[]])[0]
        except Exception as e:
            logging.exception("Error recuperando memoria: %s", e)

    memory_text = "\n".join(memory_docs[-10:])

    # =============================
    # 3. Obtener la última pregunta
    # =============================
    question = ""
    for m in reversed(messages):
        if m["role"] == "user":
            question = m["content"]
            break

    # =============================
    # 4. Generar respuesta con memoria
    # =============================
    try:
        prompt = memory_prompt.format(memory=memory_text, input=question)
        answer = await llm(prompt)
    except Exception as e:
        logging.exception("Error generando respuesta LLM: %s", e)
        answer = "No pude generar una respuesta."

    state.setdefault("messages", []).append(
        {"role": "assistant", "content": answer}
    )

    return state
