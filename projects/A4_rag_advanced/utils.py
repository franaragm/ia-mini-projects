import hashlib
from .chroma_client import collection

# Genera un hash único para un texto (para identificar chunks).
def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# Comprueba si un chunk ya está almacenado en la colección.
def is_chunk_indexed(chunk_id: str) -> bool:
    try:
        existing = collection.get(ids=[chunk_id])
        return bool(existing and existing["ids"])
    except Exception:
        return False
    
# Convierte metadatos y distancias en una lista de fuentes formateadas.
def format_sources(metadatas: list, distances: list) -> list:
    formatted = []
    for meta, dist in zip(metadatas, distances):
        # Convertir distancia a similitud (asumiendo distancia >= 0)
        similarity = 1 / (1 + dist)
        formatted.append({
            "source": meta.get("source", "desconocido"),
            "score": round(similarity, 4) # Redondear a 4 decimales
        })
    return formatted
