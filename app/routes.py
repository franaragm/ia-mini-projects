from fastapi import APIRouter
from .services.llm_client import llm
from projects.A1_chat_structured.router import router as a1_router
from projects.A2_output_parser.router import router as a2_router
from projects.A3_rag_basic.router import router as a3_router
from projects.A3_rag_basic_v2.router import router as a3v2_router
from projects.A4_rag_advanced.router import router as a4_router
from projects.A4_rag_advanced_v2.router import router as a4v2_router
from projects.A5_chains_routers.router import router as a5_router


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
router.include_router(a2_router)
router.include_router(a3_router)
router.include_router(a3v2_router)
router.include_router(a4_router)
router.include_router(a4v2_router)
router.include_router(a5_router)

