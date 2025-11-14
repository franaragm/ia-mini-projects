import os

# ==========================================================
# Configuración base global compartida entre todos los proyectos.
# Define rutas y parámetros comunes para LLM, RAG y almacenamiento.
# ==========================================================

# === Rutas base ===

# Ruta absoluta a la raíz del repositorio
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Carpeta global compartida de bases vectoriales persistentes (ChromaDB)
CHROMA_PATH = os.path.join(ROOT_DIR, "chroma_db")

# Carpeta de proyectos
PROJECTS_PATH = os.path.join(ROOT_DIR, "projects")

# Carpeta de aplicación común (FastAPI, servicios, utilidades)
APP_PATH = os.path.join(ROOT_DIR, "app")


# === Configuración técnica compartida ===

# Modelo de embeddings por defecto (SentenceTransformers)
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Modelo LLM por defecto (para OpenRouter / OpenAI compatible)
DEFAULT_LLM_MODEL = "meta-llama/llama-3.3-8b-instruct:free"
