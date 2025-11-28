from sentence_transformers import SentenceTransformer
from app.services.llm_client import llm
from config_base import DEFAULT_EMBEDDING_MODEL
from projects.A4_rag_advanced_v2.chroma_client import collection
from .prompts import rag_prompt

# Modelo de embeddings
model = SentenceTransformer(DEFAULT_EMBEDDING_MODEL)

# Recupera contexto relevante desde la colección Chroma del proyecto A4_rag_advanced_v2
def retrieve_context(question: str, n_results: int = 3) -> str:
    # Convertir pregunta → embedding
    query_vec = model.encode([question]).tolist()[0]
    
    # Consultar la colección en ChromaDB del proyecto A4_rag_advanced_v2
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results
    )
    
    # Extraer documentos (si no existen, usar listas vacías)
    retrieved_docs = results.get("documents", [[]])[0]
    
    return "\n\n".join(retrieved_docs)

# Pipeline RAG: recuperación y respuesta
# async def rag_chain(question: str):
#     context = retrieve_context(question)
#     prompt = rag_prompt.format(context=context, input=question)
#     return await llm(prompt)
