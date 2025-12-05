from typing import List, Dict, Any, Union
import uuid
import logging
from .schemas import ChatState
from app.services.llm_client import llm
from .prompts import memory_prompt, memory_preparation_prompt
from .chroma_client import collection
from .utils import clean_memory_text

logger = logging.getLogger(__name__)

async def call_llm_node(state: Union[ChatState, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Nodo principal del grafo encargado de:
    - Normalizar el estado entrante (dict o Pydantic)
    - Preparar memoria nueva con ayuda de un LLM
    - Guardar memoria del usuario en ChromaDB
    - Consultar memoria previa relevante
    - Generar respuesta usando dicha memoria
    - Devolver un estado consistente para el siguiente nodo

    Este nodo es el corazón del sistema de memoria.
    """

    # ======================================================
    # 1. Normalizar el estado recibido (puede ser dict o ChatState)
    # ======================================================
    # Extraemos user_id, mensajes, summary y meta sin importar el formato
    if isinstance(state, dict):
        _user_id = state.get("user_id")
        _messages = state.get("messages") or []
        _summary = state.get("summary")
        _meta = state.get("meta") or {}
    else:
        # Si viene un ChatState (Pydantic)
        _user_id = getattr(state, "user_id", None)
        _messages = getattr(state, "messages", []) or []
        _summary = getattr(state, "summary", None)
        _meta = getattr(state, "meta", {}) or {}

    # ======================================================
    # 2. Normalizar mensajes → convertirlos a dicts estándar
    # ======================================================
    # LangGraph y Chroma deben trabajar con mensajes homogéneos
    msgs: List[Dict[str, str]] = []
    for m in _messages:
        if isinstance(m, dict):
            role = m.get("role")
            content = m.get("content")
        else:
            role = getattr(m, "role", None)
            content = getattr(m, "content", None)

        # Solo añadimos mensajes válidos
        if role and content is not None:
            msgs.append({"role": role, "content": content})

    # ======================================================
    # 3. Preparar memoria mediante LLM (memory_preparation_prompt)
    #    - Se extrae la parte relevante del último mensaje del usuario
    #    - El LLM destila la información para almacenarla limpia
    # ======================================================
    if _user_id:
        try:
            # Buscar el último mensaje enviado por el usuario
            user_last_msg = ""
            for m in reversed(msgs):
                if m["role"] == "user":
                    user_last_msg = m["content"]
                    break

            # Enviar ese mensaje al prompt de preparación de memoria
            prep_prompt = memory_preparation_prompt.format(input=user_last_msg)
            prepared_memory = await llm(prep_prompt)
            prepared_memory = clean_memory_text(prepared_memory)

            # Guardar solo si el LLM devuelve algo útil
            if prepared_memory:
                collection.add(
                    documents=[prepared_memory],
                    metadatas=[{"user_id": _user_id}],
                    ids=[f"{_user_id}_{uuid.uuid4().hex}"]
                )
        except Exception as e:
            logger.exception("Error guardando memoria del usuario en ChromaDB: %s", e)

    # ======================================================
    # 4. Recuperar memoria existente del usuario
    #    - Se consulta ChromaDB por todas sus memorias
    #    - Nos quedamos con las últimas 10 para el prompt
    # ======================================================
    memory_docs: List[str] = []
    if _user_id:
        try:
            results = collection.query(
                query_texts=[""],   # consulta vacía → trae todas las memorias del user
                n_results=100,
                where={"user_id": _user_id}
            )

            # results["documents"] es una lista de listas -> accedemos al primer grupo
            memory_docs = results.get("documents", [[]])[0]
        except Exception as e:
            logger.exception("Error recuperando memoria para prompt: %s", e)

    # Memoria concatenada (solo últimas 10 entradas)
    memory_text = "\n".join(memory_docs[-10:] or [])

    # ======================================================
    # 5. Determinar la pregunta del usuario real
    #    (puede venir desde meta o desde mensajes)
    # ======================================================
    question = _meta.get("last_user_question", "")
    if not question:
        for m in reversed(msgs):
            if m["role"] == "user":
                question = m["content"]
                break

    # ======================================================
    # 6. Generar respuesta del LLM usando memoria + pregunta
    # ======================================================
    try:
        prompt = memory_prompt.format(memory=memory_text, input=question)
        answer = await llm(prompt)

        # Aseguramos que sea string
        if not isinstance(answer, str):
            answer = str(answer)

    except Exception as e:
        logger.exception("Error llamando al LLM: %s", e)
        answer = "Error al generar la respuesta."

    # ======================================================
    # 7. Construir el nuevo estado para el grafo
    # ======================================================
    assistant_msg = {"role": "assistant", "content": answer}

    # Añadimos el mensaje del asistente al historial
    new_msgs = msgs + [assistant_msg]

    # Actualizamos metadatos
    new_meta = dict(_meta) if _meta else {}
    new_meta["last_assistant_message"] = answer
    new_meta["last_user_question"] = question

    # Devolvemos un estado totalmente normalizado en formato dict
    return {
        "user_id": _user_id,
        "messages": new_msgs,
        "summary": _summary,
        "meta": new_meta,
    }
