from fastapi import APIRouter
from app.services.llm_client import llm
from .rag import build_index_from_folder, retrieve
from .prompts import rag_prompt
from .utils import safe_json_parse
from .schemas import QueryRequest, QueryResponse
import threading

router = APIRouter(prefix="/a3v2", tags=["A3 - RAG Básico v2"])

DATA_PATH = "projects/A3_rag_basic_v2/data"

# Indexado automático en segundo plano al cargar el módulo 
def _auto_build_index():
    try:
        build_index_from_folder(DATA_PATH)
    except Exception as e:
        print(f"[RAG] Error durante el indexado automático: {e}")

# Lanzamos el indexado en un hilo para no bloquear FastAPI al arrancar
threading.Thread(target=_auto_build_index, daemon=True).start()

@router.post(
    "/query",
    summary="Realiza una consulta utilizando RAG básico mejorado",
    description="""
    Realiza una consulta utilizando un enfoque de Recuperación Augmentada por Generación (RAG) básico.
    1. **Carga automática de documentos** desde una carpeta (`/data`).
    2. **Limpieza y fragmentación de texto** (chunking) para mejorar las búsquedas.
    3. **Reindexación incremental** (no duplica documentos ya indexados).
    4. **Búsqueda semántica top-k** configurable.
    5. **Uso del LLM con contexto RAG** para generar la respuesta.
    6. **Estructura clara con logs y validaciones**.
    """,
    response_description="Respuesta generada y documentos fuente",
    response_model=QueryResponse
)
async def query_rag(req: QueryRequest):
    # Recuperamos documentos relevantes del índice vectorial
    context_docs = retrieve(req.question, top_k=3)
    context = "\n".join(context_docs)

    # Creamos el prompt que incluye el contexto + pregunta
    prompt = rag_prompt.format(context=context, question=req.question)

    # Consultamos el modelo LLM (vía OpenRouter)
    response = await llm(prompt)

    # Parseamos la salida (puede ser JSON válido o texto plano)
    parsed = safe_json_parse(response)

    # Si es un objeto Pydantic, convertimos a dict
    if hasattr(parsed, "model_dump"):
        parsed = parsed.model_dump()

    # Añadimos las fuentes usadas en la respuesta
    parsed["sources"] = context_docs

    # Retornamos una respuesta validada según el esquema Pydantic
    return QueryResponse(**parsed)