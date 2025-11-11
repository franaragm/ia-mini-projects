import os

# Función para cargar documentos de un directorio
def load_documents(data_path: str):
    docs = []
    for file in os.listdir(data_path):
        full_path = os.path.join(data_path, file)
        if file.endswith(".txt"):
            with open(full_path, "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs
