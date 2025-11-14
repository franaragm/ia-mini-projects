import chromadb
from .config import COLLECTION_NAME, CHROMA_PATH

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)
