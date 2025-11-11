from fastapi import APIRouter
from app.services.llm_client import llm
from .prompts import chat_template
from .schemas import ChatRequest, ChatResponse
import json

router = APIRouter(prefix="/a1", tags=["A1 - Chat estructurado"])

@router.post(
    "/chat",
    summary="Chat con respuesta estructurada en JSON",
    description="""
    Recibe un mensaje de usuario, lo envía a un modelo de lenguaje y devuelve una respuesta en formato JSON válido.
    El JSON incluye la respuesta del asistente, el tono y metadatos sobre el modelo utilizado.
    """,
    response_description="JSON estructurado con la respuesta del asistente",
    response_model=ChatResponse
)
async def structured_chat(req: ChatRequest):
    prompt = chat_template.format(user_message=req.message)
    raw = await llm(prompt)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "El modelo devolvió un JSON inválido",
            "raw_response": raw
        }
        
    try:
        data = ChatResponse(**data)
    except Exception as e:
        return {
            "error": "La estructura JSON no cumple el esquema esperado",
            "details": str(e),
            "raw_data": data
        }

    return data
