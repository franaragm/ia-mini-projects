from fastapi import APIRouter
from app.services.llm_client import llm
from .prompts import intent_prompt, today
from .schemas import IntentRequest, IntentResponse
import json

router = APIRouter(prefix="/a2", tags=["A2 - Output Parser & Validación"])

@router.post(
    "/parse-intent",
    summary="Analiza el mensaje del usuario y devuelve la intención en un JSON validado",
    description="""
    Recibe un mensaje de usuario, lo envía a un modelo de lenguaje para analizar la intención y devuelve un JSON estructurado y validado con Pydantic.
    Se puede usar para crear tareas, actualizar tareas o consultar el estado de tareas.
    Si se indica una fecha relativa, se calcula en base a la fecha actual.
    """,
    response_description="JSON estructurado con la respuesta del asistente",
    response_model=IntentResponse
)
async def parse_intent(req: IntentRequest):
    prompt = intent_prompt.format(user_message=req.message, today=today)
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
