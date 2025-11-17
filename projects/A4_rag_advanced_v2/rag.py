from sentence_transformers import SentenceTransformer
from app.services.llm_client import llm
from .config import COLLECTION_NAME, EMBEDDING_MODEL
from .chroma_client import collection
from .loader import load_documents, split_documents
from .prompts import rag_prompt
from .utils import hash_text, is_chunk_indexed, format_sources
from .scraper import scrape_webpage

# Modelo de embeddings del proyecto
model = SentenceTransformer(EMBEDDING_MODEL)

# ==========================================================
# Construcción del índice (local + web) (siempre se reconstruye si hay nuevos documentos)
# ==========================================================

# Crea embeddings y guarda documentos nuevos en la colección persistente.
def build_vectorstore(urls: list[str] = None):
    print("📌 Iniciando indexado...")
    
    # list[Document] con todos los chunks sin procesar
    raw_chunks = []
    
    # Documentos locales desde /data/
    raw_chunks.extend(split_documents(load_documents()))
    
    # Documentos scrapeados desde URLs (si se proporcionan)
    if urls:
        for url in urls:
            print(f"Scrapeando y procesando: {url}")
            scraped_docs = scrape_webpage(url)
            raw_chunks.extend(split_documents(scraped_docs))
    
    if not raw_chunks:
        print("No se encontraron documentos para procesar.")
        return collection
    
    # Lista de nuevos chunks a indexar
    new_chunks = []

    # Recorrer raw_chunks que es un list[Document] con documentos fragmentados y verificar duplicados, 
    # cada elemento Document de la lista contiene las propiedades page_content y metadata
    for chunk in raw_chunks:
        chunk_text = chunk.page_content.strip() # Limpiar espacios en blanco alrededor y verificar texto vacío
        if not chunk_text:
            continue

        chunk_id = hash_text(chunk_text)
        if not is_chunk_indexed(chunk_id):
            new_chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {"source": chunk.metadata.get("source", "desconocido")}
            })

    # Si hay nuevos chunks, calcular embeddings y añadirlos
    if new_chunks:
        print(f"Generando {len(new_chunks)} nuevos embeddings...")
        
        chunks_text = [item["text"] for item in new_chunks]
        ids = [item["id"] for item in new_chunks]
        metadatas = [item["metadata"] for item in new_chunks]
        vectors = model.encode(chunks_text).tolist()
        
        collection.add(
            ids=ids,
            documents=chunks_text,
            embeddings=vectors,
            metadatas=metadatas
        )
        print(f"{len(new_chunks)} fragmentos añadidos a '{COLLECTION_NAME}'.")
    else:
        print("No se encontraron nuevos fragmentos para indexar (colección ya actualizada).")

    return collection

# ==============================================
# Compresión contextual
# ==============================================

# Usa el LLM para comprimir múltiples documentos en un solo contexto.
async def compress_context(docs: list[str]) -> str:
    joined = "\n\n".join(docs)

    prompt = f"""
        Reduce y resume el siguiente texto manteniendo solo la información esencial para contestar preguntas:

        {joined}
    """

    compressed = await llm(prompt)
    return compressed

# ==========================================================
# Recuperación de contexto
# ==========================================================

# Recupera contexto relevante desde la colección Chroma.
def retrieve_context(question: str, n_results: int = 3) -> (tuple[list[str], list[dict]]):
    # Convertir pregunta → embedding
    query_vec = model.encode([question]).tolist()[0]

    # Consultar la colección en ChromaDB
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results
    )

    # Extraer documentos y metadatos (si no existen, usar listas vacías), distancias para posibles futuros usos
    retrieved_docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    
    # Formatear las fuentes para la respuesta
    sources = format_sources(metadatas, distances)

    return retrieved_docs, sources


# ==========================================================
# Llamada al modelo LLM
# ==========================================================

# Genera una respuesta del LLM usando el contexto relevante.
async def _answer_with_llm(context: str, question: str) -> str:
    prompt = rag_prompt.format(context=context, question=question)
    response = await llm(prompt)
    return response.strip()


# ==========================================================
# Pipeline principal RAG
# ==========================================================

# Ejecuta el pipeline RAG completo: recuperación, compresión y respuesta.
async def answer_query(question: str):
    docs, sources = retrieve_context(question)
    
    # compresión contextual
    context_compressed = await compress_context(docs)
    
    answer = await _answer_with_llm(context_compressed, question)
    return {"answer": answer, "sources": sources}
