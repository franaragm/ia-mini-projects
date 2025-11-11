from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2") # Modelo ligero para embeddings

client = chromadb.PersistentClient(path="./chroma_db") # Cliente persistente para almacenar datos
collection = client.get_or_create_collection("a3_docs") # Colección para documentos

def build_index(documents):
    vectors = model.encode(documents).tolist() # Convierte los documentos a vectores
    ids = [f"doc_{i}" for i in range(len(documents))] # Genera IDs únicas para cada documento
    collection.add(documents=documents, embeddings=vectors, ids=ids) # Añade los documentos y sus vectores a la colección

def retrieve(question: str):
    query_vec = model.encode([question]).tolist()[0] # Convierte la pregunta a vector
    results = collection.query(query_embeddings=[query_vec], n_results=3) # Recupera los 3 documentos más similares
    return results["documents"][0] # Devuelve los documentos recuperados
