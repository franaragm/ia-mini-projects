from fastapi import APIRouter
from .services.llm_client import ask_model

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/test-llm")
async def test_llm():
    answer = await ask_model("Dime una frase corta divertida como un astronauta para confirmar conexión.")
    return {"response": answer}
