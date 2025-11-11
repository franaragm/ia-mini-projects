from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_client import llm
from .loader import load_documents
from .rag import build_index, retrieve
from .prompts import rag_prompt
from .schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/a3", tags=["A3 - RAG básico"])

DATA_PATH = "projects/A3_rag_basic/data"

# Construye el índice on startup:
documents = load_documents(DATA_PATH)
build_index(documents)

@router.post(
    "/ask",
    summary="Realiza una pregunta utilizando RAG básico",
    description="""
    Realiza una pregunta utilizando un enfoque de Recuperación Augmentada por Generación (RAG) básico.
    1. Recupera documentos relevantes basados en la pregunta del usuario.
    2. Usa un modelo de lenguaje para generar una respuesta basada en esos documentos.
    """,
    response_description="Respuesta generada y documentos fuente",
    response_model=QueryResponse,
)
async def ask_rag(req: QueryRequest):
    relevant_docs = retrieve(req.question) # Recupera documentos relevantes
    context = "\n\n".join(relevant_docs) # Prepara el contexto para el prompt
    prompt = rag_prompt.format(context=context, question=req.question) # Formatea el prompt
    answer = await llm(prompt) # Llama al modelo de lenguaje
    return {"response": answer.strip(), "sources": relevant_docs}
