import threading
from fastapi import APIRouter
from .config import URLS_TO_SCRAPE
from .schemas import QueryRequest, QueryResponse, SourceDocument
from .rag import build_vectorstore, answer_query

router = APIRouter(prefix="/a4v2", tags=["A4 - RAG Avanzado con web scraping, compresión contextual y fuentes puntuadas"])

# Lanzamos indexado en segundo plano al importar el router
def _auto_build_index():
    try:
        print("Construyendo índice RAG avanzado en background...")
        build_vectorstore(URLS_TO_SCRAPE)
        print("Índice RAG avanzado listo.")
    except Exception as e:
        print(f"[RAG] Error durante el indexado automático: {e}")

threading.Thread(target=_auto_build_index, daemon=True).start()


@router.post(
    "/query",
    summary="RAG Avanzado con web scraping, compresión contextual y fuentes puntuadas",
    description="""
    Implementar un pipeline **RAG completo** usando **LangChain**, con:
    - Carga automática de documentos locales.
    - Web scraping de URLs especificadas.
    - Compresión contextual.
    - Chunking inteligente.
    - Indexación persistente con **ChromaDB**.
    - Recuperación semántica.
    - Generación de respuestas con contexto real.
    """,
    response_description="Respuesta generada y documentos fuente",
    response_model=QueryResponse
)
async def query_rag(req: QueryRequest):
    result = await answer_query(req.question)
    # Formatear las fuentes según el esquema Pydantic
    formatted_sources = [SourceDocument(**src) for src in result["sources"]]
    return QueryResponse(
        answer=result["answer"],
        sources=formatted_sources,
    )
