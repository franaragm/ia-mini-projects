from fastapi import APIRouter
from .services.llm_client import llm
from projects.A1_chat_structured.main import router as a1_router

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/test-llm")
async def test_llm():
    answer = await llm("Dime una frase corta divertida como un astronauta para confirmar conexión.")
    return {"response": answer}

# Rutas de los mini-proyectos
router.include_router(a1_router)
