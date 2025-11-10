from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.llm_client import llm
from .prompts import intent_prompt
from .schemas import IntentRequest, IntentResponse
import json

router = APIRouter(prefix="/a2", tags=["A2 - Output Parser & Validación"])


@router.post("/parse-intent", response_model=IntentResponse)
async def parse_intent(req: IntentRequest):
    prompt = intent_prompt.format(user_message=req.message)
    raw = await llm(prompt)

    # Intentamos parsear JSON del modelo
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "El modelo devolvió un JSON inválido",
            "raw_response": raw
        }

    # Validamos estructura con Pydantic
    try:
        parsed = IntentResponse(**data)
    except Exception as e:
        return {
            "error": "La estructura JSON no cumple el esquema esperado",
            "details": str(e),
            "raw_data": data
        }

    return parsed
