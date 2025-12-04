from typing import List, Dict, Any, Union
import uuid
import logging

from .schemas import ChatState, Message
from app.services.llm_client import llm
from .prompts import memory_prompt, memory_preparation_prompt
from .chroma_client import collection

logger = logging.getLogger(__name__)


async def call_llm_node(state: Union[ChatState, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Nodo del grafo que maneja:
    - Normalización del estado
    - Preparación de memoria mediante LLM
    - Consulta de memoria más reciente
    - Llamada al LLM para generar respuesta
    - Persistencia de memorias de usuario en ChromaDB
    - Devolver estado consistente (dicts, no Pydantic)
    """

    # -----------------------------
    # Normalizar estado (dict o ChatState)
    # -----------------------------
    if isinstance(state, dict):
        _user_id = state.get("user_id")
        _messages = state.get("messages") or []
        _summary = state.get("summary")
        _meta = state.get("meta") or {}
    else:
        _user_id = getattr(state, "user_id", None)
        _messages = getattr(state, "messages", []) or []
        _summary = getattr(state, "summary", None)
        _meta = getattr(state, "meta", {}) or {}

    # -----------------------------
    # Normalizar mensajes → lista de dicts
    # -----------------------------
    msgs: List[Dict[str, str]] = []
    for m in _messages:
        if isinstance(m, dict):
            role = m.get("role")
            content = m.get("content")
        else:
            role = getattr(m, "role", None)
            content = getattr(m, "content", None)
        if role and content is not None:
            msgs.append({"role": role, "content": content})

    # -----------------------------
    # Preparar memoria del usuario usando LLM
    # -----------------------------
    if _user_id:
        try:
            # Último mensaje del usuario
            user_last_msg = ""
            for m in reversed(msgs):
                if m["role"] == "user":
                    user_last_msg = m["content"]
                    break

            # Generar texto de memoria limpio usando memory_preparation_prompt
            prep_prompt = memory_preparation_prompt.format(input=user_last_msg)
            prepared_memory = await llm(prep_prompt)
            prepared_memory = prepared_memory.strip()

            # Guardar solo si hay contenido relevante
            if prepared_memory:
                collection.add(
                    documents=[prepared_memory],
                    metadatas=[{"user_id": _user_id}],
                    ids=[f"{_user_id}_{uuid.uuid4().hex}"]
                )
        except Exception as e:
            logger.exception("Error guardando memoria del usuario en ChromaDB: %s", e)

    # -----------------------------
    # Recuperar la memoria más reciente para la respuesta
    # -----------------------------
    memory_docs: List[str] = []
    if _user_id:
        try:
            results = collection.query(
                query_texts=[""],  # vacía para obtener todas las memorias del user
                n_results=100,
                where={"user_id": _user_id}
            )
            memory_docs = results.get("documents", [[]])[0]
        except Exception as e:
            logger.exception("Error recuperando memoria para prompt: %s", e)

    memory_text = "\n".join(memory_docs[-10:] or [])

    # -----------------------------
    # Determinar pregunta del usuario
    # -----------------------------
    question = _meta.get("last_user_question", "")
    if not question:
        for m in reversed(msgs):
            if m["role"] == "user":
                question = m["content"]
                break

    # -----------------------------
    # Llamar al LLM para generar respuesta
    # -----------------------------
    try:
        prompt = memory_prompt.format(memory=memory_text, input=question)
        answer = await llm(prompt)
        if not isinstance(answer, str):
            answer = str(answer)
    except Exception as e:
        logger.exception("Error llamando al LLM: %s", e)
        answer = "Error al generar la respuesta."

    # -----------------------------
    # Preparar nuevo estado
    # -----------------------------
    assistant_msg = {"role": "assistant", "content": answer}
    new_msgs = msgs + [assistant_msg]

    new_meta = dict(_meta) if _meta else {}
    new_meta["last_assistant_message"] = answer
    new_meta["last_user_question"] = question

    return {
        "user_id": _user_id,
        "messages": new_msgs,
        "summary": _summary,
        "meta": new_meta,
    }
