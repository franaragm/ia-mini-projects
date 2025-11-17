import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Ruta al directorio de datos
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

# Carga todos los documentos TXT y MD desde /data/
def load_documents():
    docs = []
    for file in os.listdir(DATA_PATH):
        if file.endswith((".txt", ".md")):
            loader = TextLoader(os.path.join(DATA_PATH, file), encoding="utf-8") # Crear cargador de texto
            docs.extend(loader.load()) # Cargar y agregar documentos
    return docs

# Divide documentos en chunks con solapamiento
def split_documents(documents, chunk_size=600, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " "]
    )
    return splitter.split_documents(documents)
