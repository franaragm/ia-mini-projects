import os
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL
from .chroma_client import collection
from .utils import hash_text

# Cargar modelo de embeddings (solo una vez)
model = SentenceTransformer(EMBEDDING_MODEL)

# Construye el índice desde una carpeta de documentos
def build_index_from_folder(folder_path: str):
    docs = []
    ids = []
    for fname in os.listdir(folder_path):
        if not fname.endswith((".txt", ".md")):
            continue
        with open(os.path.join(folder_path, fname), "r", encoding="utf-8") as f:
            content = f.read()

        # Fragmentar en chunks de 400 caracteres
        chunks = [content[i:i+400] for i in range(0, len(content), 400)]
        for chunk in chunks:
            doc_id = hash_text(chunk)
            if doc_id not in collection.get(ids=[doc_id])["ids"]:
                docs.append(chunk)
                ids.append(doc_id)

    if docs:
        vectors = model.encode(docs).tolist()
        collection.add(documents=docs, embeddings=vectors, ids=ids)
        print(f"{len(docs)} fragmentos indexados correctamente.")
    else:
        print("No hay nuevos documentos para indexar.")

# Recupera los documentos más relevantes al prompt del usuario
def retrieve(question: str, top_k: int = 3):
    query_vec = model.encode([question]).tolist()[0]
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)
    documents = results.get("documents", [[]])[0]
    return documents