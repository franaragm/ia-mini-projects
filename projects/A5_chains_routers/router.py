from fastapi import APIRouter
from .schemas import A5Request, A5Response
from .chains import run_router_chain

router = APIRouter(
    prefix="/a5",
    tags=["A5 - Chains y Routers (LangChain avanzado)"]
)

@router.post(
    "/query",
    summary="Pipeline con clasificación, enrutado dinámico y cadenas secuenciales",
    description="""
    Implementar un pipeline avanzado usando **LangChain** que incluya:
    - Clasificación de la intención del usuario.
    - Enrutado dinámico a diferentes cadenas (RAG, código, resumen, matemáticas, general).
    - Uso de cadenas secuenciales para tareas complejas.
    """,
    response_description="Respuesta generada y cadena usada",
    response_model=A5Response
)
async def query(req: A5Request):
    result = await run_router_chain(req.question)
    return A5Response(**result)