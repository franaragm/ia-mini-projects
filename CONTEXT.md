# **🧠 CONTEXTO GLOBAL DEL REPOSITORIO — Mini-Proyectos LangChain Lab**

Este repositorio contiene una colección de **mini-proyectos progresivos**, cada uno enfocado en un componente distinto del ecosistema LLM: prompts, output parsing, RAG, embeddings, scrapers, chains, routers y agentes.

El servidor está construido sobre **FastAPI**, con un diseño modular donde cada mini-proyecto es independiente, pero todo comparte la misma infraestructura base.

---

# 🏗️ **ARQUITECTURA GENERAL DEL REPOSITORIO**

```
mini-projects-langchain/
│
├── README.md
├── CONTEXT_REPO.md            ← ESTE ARCHIVO (contexto global)
├── config_base.py             ← Config global compartida
├── requirements.txt
├── .env.example
│
├── app/                       ← Servidor FastAPI + utilidades globales
│   ├── main.py
│   ├── routes.py
│   └── services/
│       ├── llm_client.py      ← Cliente LLM (OpenRouter)
│       ├── utils.py
│       └── ...
│
└── projects/                  ← Mini-proyectos aislados
    ├── A1_chat_structured/
    ├── A2_output_parser/
    ├── A3_rag_basic/
    ├── A3_rag_basic_v2/
    ├── A4_rag_advanced/
    ├── A4_rag_advanced_v2/
    ├── A5_chains_routers/
    ├── A5_memory/
    └── …
```

**requeriments.txt actual**

```
fastapi
uvicorn[standard]

# Núcleo de LangChain (PromptTemplate, OutputParser, etc.)
langchain-core
langchain
langchain-text-splitters
langchain-openai

# Integraciones generales y utilidades (sin modelos OpenAI)
langchain-community

# Cliente OpenAI compatible con OpenRouter
openai

# Para usar modelos de embeddings locales (MiniLM, etc.)
sentence-transformers

# Vector DB local para RAG
chromadb

# Scraping web
requests
beautifulsoup4

# Utilidades comunes
python-dotenv
pydantic
httpx

# Validación de correos (elimina warning de FastAPI/Pydantic)
email-validator
```

---

# 🔧 **DESCRIPCIÓN DE LA CAPA BASE DEL SERVIDOR**

## **`app/main.py`**

Configura FastAPI:

* URLs de documentación (`/docs`) sólo en entorno `dev`
* Metadatos (nombre, versión, contacto)
* Incluye el router principal

## **`app/routes.py`**

Define:

* Endpoints globales (`/health`, `/test-llm`)
* Registro automático de todos los mini-proyectos:

  ```python
  router.include_router(a1_router)
  router.include_router(a2_router)
  ...
  ```

## **`app/services/llm_client.py`**

Proporciona **dos clientes diferentes**:

### 1. `llm(prompt: str)`

Cliente simplificado para obtener **solo texto** (sin LangChain).
Ideal para proyectos básicos o utilidades.

### 2. `llm_chain()`

Devuelve `ChatOpenAI` para integrarse en:

* LCEL
* RouterChain
* Sequential chains
* Agents
* Tools con funciones reales

Ambos clientes usan OpenRouter (modelos GPT-OSS, Nemotron, etc.).

---

# ⚙️ **CONFIGURACIÓN GLOBAL — `config_base.py`**

Define:

* Rutas absolutas del repo
* Ruta centralizada de bases vectoriales
* Modelo de embeddings global (`all-MiniLM-L6-v2`)
* LLM por defecto y fallback
* Paths de `projects/` y `app/`

Todos los mini-proyectos importan desde aquí para evitar duplicación:

```python
from config_base import CHROMA_PATH, DEFAULT_EMBEDDING_MODEL
```

---

# 🧩 **PATRÓN DE DISEÑO DE CADA MINI-PROYECTO**

Cada mini-proyecto se estructura con la misma arquitectura:

```
A4_rag_advanced_v2/
│
├── router.py               ← Endpoint FastAPI
├── config.py               ← Config específica del mini proyecto
├── schemas.py              ← Pydantic (Request/Response)
├── prompts.py              ← PromptTemplates usados
├── rag.py                  ← Lógica principal (RAG, embeddings, compresión)
├── chroma_client.py        ← Inicialización de colección Chroma
├── loader.py               ← Carga de documentos locales
├── scraper.py              ← Web scraping (opcional)
├── utils.py                ← Hash, formateo de fuentes, etc.
└── data/                   ← Documentos locales a indexar
```

### **Archivos frecuentes:**

### ✔ `router.py`

Define:

* Rutas del mini-proyecto
* Indexación automática al arrancar
* Conversión entre modelos Pydantic y outputs del pipeline

### ✔ `schemas.py`

Estándar común para todos los mini-proyectos:

```python
class QueryRequest(BaseModel):
    question: str

class SourceDocument(BaseModel):
    source: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
```

### ✔ `config.py`

Config local del proyecto:

* Nombre de colección
* URLs a scrapear
* Parámetros de embeddings
* Ruta de almacenamiento

### ✔ `prompts.py`

PromptTemplates para:

* Clasificador de intención
* Prompt general
* Prompt de RAG
* Prompt de resumen
* Prompt de código
* Prompt matemático

### ✔ `chroma_client.py`

Inicializa la colección con:

```python
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)
```

### ✔ `loader.py`

Carga documentos desde `/data`, los divide con `RecursiveCharacterTextSplitter`.

### ✔ `scraper.py`

Extrae HTML de URLs, limpia scripts/style, devuelve `Document`.

### ✔ `utils.py`

Funciones auxiliares como:

* `hash_text()`
* `is_chunk_indexed()`
* `format_sources()`

---

# 📚 **DESCRIPCIÓN RESUMIDA DE LOS MINI-PROYECTOS**

### **A1 – Chat estructurado**

Primeros prompts, respuestas controladas.

### **A2 – Output Parser**

Validación estricta con Pydantic / JSON.

### **A3 – RAG Básico**

Cargar documentos → fragmentarlos → indexar → recuperar contexto.

### **A3 V2 – RAG Básico Mejorado**

Separadores custom + limpieza + mejor chunking.

### **A4 – RAG Avanzado**

Fuentes + puntajes + anti-alucinación rígida.

### **A4 V2 – RAG con Web Scraping**

* Carga local + scrapeo web
* Compresión contextual
* Puntajes normalizados

### **A5 – Chains & Routers**

Arquitectura completa:

```
Pregunta → Clasificador → Router → (General / Summary / Code / Math / RAG)
```

con LCEL (`|` operator) y `RunnableLambda`.

### **A5 – Memory**

Buffers, resumen incremental, memoria contextual.

---

# 🧠 **DIRECTRICES PARA CREAR UN NUEVO MINI-PROYECTO**

Cada nuevo mini-proyecto debe seguir este template:

```
projects/A6_nombre/
│
├── router.py
├── config.py
├── prompts.py
├── logic.py o rag.py o agent.py (según el caso)
├── schemas.py
├── utils.py
├── chroma_client.py (si usa vectores)
├── loader.py / scraper.py (si aplica)
└── data/
```

### **Reglas de arquitectura:**

1. **Jamás duplicar llm_client**: usar siempre el cliente global.
2. **Nunca crear su propio chromadb** → usar `CHROMA_PATH`.
3. **Un mini-proyecto = un endpoint FastAPI bien aislado**.
4. **Prompts siempre en `prompts.py`.**
5. **Schemas siempre en `schemas.py`.**
6. **Toda lógica en un archivo separado (ej: `rag.py`, `agent.py`, `chain.py`).**
7. **Mantener máxima modularidad.**
8. **Si usa embeddings → usar modelo global salvo que tengas buena razón.**

---

# 🔥 **DIRECTRICES PARA CÓMO RESPONDEN LOS LLM EN ESTE REPO**

### ✔ Clasificación de intención (A5)

El LLM debe:

* Responder solo: `general`, `rag`, `summary`, `code`, `math`
* No agregar nada más
* En caso de duda → `general`

### ✔ RAG

Reglas:

* No puede inventar nada
* Solo usa el contexto recuperado
* Si no hay suficiente contexto:

```
"Sin suficiente información en la documentación para responder."
```

* Sí puede sintetizar (no solo copiar)
* No puede rellenar huecos con conocimiento general

### ✔ Code

Solo código correcto y explicaciones cuando proceda.

### ✔ Summary

Resumen objetivo basado en texto proporcionado por el usuario.

### ✔ General

Conversación natural.

---

# 🧱 **ESTÁNDAR DE PATRONES PARA CHAINS (A5)**

### Ejemplo típico:

```python
chain = (
    preprocess_text
    | classifier_chain
    | router
    | selected_chain
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "..."} )
)
```

### Reglas:

* Usar LCEL (`|`)
* No usar clases antiguas de LangChain (ej: `LLMChain`, `RouterChain`, `TransformChain`)
* Preferir `RunnableLambda` y `ChatPromptTemplate`

---

# 🧩 **RAG Pipeline estándar del repo**

1. Cargar documentos (`loader.py`)
2. Dividir documentos (`split_documents`)
3. Limpiar y hash para evitar duplicados
4. Crear embedding con `SentenceTransformers`
5. Persistir en ChromaDB
6. Recuperar contexto
7. (Opcional) Compresión contextual
8. Ejecutar prompt RAG

---

# 🧪 **Pruebas y desarrollo**

* Ejecutar servidor:

```
uvicorn app.main:app --reload --port 8000
```

* Usar `/docs` para probar endpoints en dev.

---

# (Extensión del contexto — **app/** completo)**

Estos archivos contenidos en app sirven para reutilizar en los miniproyectos , nop volver hacer estas funcionalidades de app/ en los mini proyectos.

**Fuente del repositorio:** `https://github.com/franaragm/ia-mini-projects`. ([GitHub][1])

---

## 📁 `app/main.py`

**Ruta:** `app/main.py`
**Función:** Punto de entrada del servidor FastAPI. Configura la aplicación, la documentación condicional (dev/prod), los metadatos y registra el router principal.

**Código (exacto, sin modificar):**

```python
from fastapi import FastAPI
from .routes import router
from .services.utils import get_env

ENV = get_env("ENV", "dev")  # dev | prod

docs_url = "/docs" if ENV == "dev" else None
redoc_url = "/redoc" if ENV == "dev" else None
openapi_url = "/openapi.json" if ENV == "dev" else None

app = FastAPI(
    title="LangChain Lab - AI Server",
    description="""
    Servidor de experimentación con modelos de IA, RAG y agentes.

    Este backend expone APIs para explorar:
    - Recuperación aumentada con generación (RAG)
    - Llamadas a modelos LLM
    - Herramientas generativas
    - Proyectos modulares de IA

    """,
    version="1.0.0",
    summary="Backend laboratorio para proyectos de IA",
    contact={
        "name": "Francisco Aragón",
        "email": "franaragonmesa@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

app.include_router(router)
```

---

## 📁 `app/routes.py`

**Ruta:** `app/routes.py`
**Función:** Router principal que registra endpoints globales (`/health`, `/test-llm`) y **incluye** los routers de cada mini-proyecto (A1..A5...). Útil para mantener la separación modular entre proyectos.

**Código (exacto, sin modificar):**

```python
from fastapi import APIRouter
from .services.llm_client import llm
from projects.A1_chat_structured.router import router as a1_router
from projects.A2_output_parser.router import router as a2_router
from projects.A3_rag_basic.router import router as a3_router
from projects.A3_rag_basic_v2.router import router as a3v2_router
from projects.A4_rag_advanced.router import router as a4_router
from projects.A4_rag_advanced_v2.router import router as a4v2_router
from projects.A5_chains_routers.router import router as a5_router


router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/test-llm")
async def test_llm():
    answer = await llm("Dime una frase corta divertida como un astronauta para confirmar conexión.")
    return {"response": answer}

# Rutas de los mini-proyectos
router.include_router(a1_router)
router.include_router(a2_router)
router.include_router(a3_router)
router.include_router(a3v2_router)
router.include_router(a4_router)
router.include_router(a4v2_router)
router.include_router(a5_router)
```

---

## 📁 `app/services/llm_client.py`

**Ruta:** `app/services/llm_client.py`
**Función:** Cliente universal para LLMs vía **OpenRouter**. Provee:

* `llm(prompt: str, model: str | None = None) -> str`: cliente async minimalista (devuelve texto).
* `llm_chain(model: str | None = None, temperature: float = 0.0) -> ChatOpenAI`: wrapper para LangChain (devuelve `ChatOpenAI` compatible con LCEL / chains).

**Código (exacto, sin modificar):**

```python
from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from .utils import get_env
from config_base import DEFAULT_LLM_MODEL, FALLBACK_LLM_MODEL

OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = get_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Cliente OpenRouter compatible con AsyncOpenAI
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

# ============================================================
# 1) Cliente simple (para proyectos casuales o endpoints básicos)
# ============================================================

# Cliente minimalista para prompts directos sin LangChain. Devuelve solo texto. Ideal para endpoints simples.
async def llm(prompt: str, model: str | None = None) -> str:
    model_to_use = model or DEFAULT_LLM_MODEL
    params = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    try:
        response = await client.chat.completions.create(model=model_to_use, **params)

    except Exception:
        # Reintento limpio usando fallback
        response = await client.chat.completions.create(model=FALLBACK_LLM_MODEL, **params)

    return response.choices[0].message.content

# ============================================================
# 2) Cliente especial para Chains LangChain
# ============================================================

# Devuelve un objeto ChatOpenAI configurado para OpenRouter. Compatible con LLMChain, RouterChain, MultiPromptChain, agentes, etc.
def llm_chain(model: str | None = None, temperature: float = 0.0,) -> ChatOpenAI:
    model_to_use = model or DEFAULT_LLM_MODEL

    llm_params = {
        "api_key": OPENROUTER_API_KEY,
        "base_url": OPENROUTER_BASE_URL,
        "temperature": temperature,
    }

    try:
        return ChatOpenAI(model=model_to_use, **llm_params)
    except Exception:
        return ChatOpenAI(model=FALLBACK_LLM_MODEL, **llm_params)
```

---

## 📁 `app/services/utils.py`

**Ruta:** `app/services/utils.py`
**Función:** Utilidades comunes del servidor; carga variables de entorno y helpers. (Nota: en tu repo existe versión `get_env` en este archivo.)

**Código (exacto, sin modificar):**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Carga .env automáticamente

def get_env(name: str, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"❌ Variable de entorno no encontrada: {name}")
    return value
```

---

## 📁 `config_base.py`

**Ruta:** `config_base.py` (archivo de configuración global)
**Función:** Define rutas y parámetros globales usados por todos los mini-proyectos (paths, modelos, colecciones persistentes).

**Código (exacto, sin modificar):**

```python
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

# Modelo LLM default y modelo LLM fallback (para OpenRouter / OpenAI compatible)
DEFAULT_LLM_MODEL = "openai/gpt-oss-20b:free"
FALLBACK_LLM_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"
```

---



# (Extensión del contexto — ejemplos de archivos incluidos en algunos mini proyectos)**

Estos ejemplos de código son solo a modo de ejemplo de como se han estructurado funcionalidades en algunos mini proyectos y a modo de estilo a seguir:

repositorio [1]: https://github.com/franaragm/ia-mini-projects "GitHub - franaragm/ia-mini-projects: LangChain Lab #OpenRouter #FastAPI"

---

## ✅ **1. `schemas.py` — Modelos Pydantic (Ejemplo real, sin modificar)**

### **Para qué sirve**

Este archivo define **las estructuras de entrada y salida de tu API** usando Pydantic.
Todos los mini-proyectos siguen este patrón:

* **QueryRequest** → lo que envía el usuario al endpoint
* **SourceDocument** → cada documento recuperado por el RAG (con similitud, fuente, etc.)
* **QueryResponse** → respuesta final que devuelve el endpoint

### **Cómo se usa**

El router lo importa y lo utiliza como `response_model`.
FastAPI convierte automáticamente tus valores Python en el formato de las clases.

---

### **A MODO DE EJEMPLO**

```python
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., example="Qué significa escrapear una página web?")

class SourceDocument(BaseModel):
    source: str = Field(..., description="Ruta o nombre del documento de origen")
    score: float = Field(..., description="Similitud o relevancia del documento recuperado")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Respuesta generada por el modelo")
    sources: list[SourceDocument] = Field(..., description="Documentos usados para generar la respuesta")
```

---

## ✅ **2. `config.py` — Configuración del mini-proyecto (Ejemplo real)**

### **Para qué sirve**

Define parámetros globales:

* **COLLECTION_NAME** → colección de ChromaDB
* **EMBEDDING_MODEL** → modelo SentenceTransformer
* **CHROMA_PATH** → carpeta donde se guardan los vectores
* **URLS_TO_SCRAPE** → URLs que se scrapearán automáticamente

### **Cómo se usa**

El archivo `rag.py` y `chroma_client.py` importan estos valores.

---

### **A MODO DE EJEMPLO**

```python
from config_base import CHROMA_PATH, DEFAULT_EMBEDDING_MODEL

COLLECTION_NAME = "a4_docs_v2"
EMBEDDING_MODEL = DEFAULT_EMBEDDING_MODEL
CHROMA_PATH = CHROMA_PATH
URLS_TO_SCRAPE = [
    "https://es.wikipedia.org/wiki/Web_scraping",
    "https://es.wikipedia.org/wiki/Base_de_datos_de_vectores",
    # Añade más URLs según sea necesario
]
```

---

## ✅ **3. `prompts.py` — Prompts del mini-proyecto**

### **Para qué sirve**

Define **TODOS los prompts del pipeline**:

* **classifier_prompt** → clasifica intención del usuario
* **general_prompt, code_prompt, summary_prompt, math_prompt**
* **rag_prompt** → prompt estricto para RAG

### **Cómo se usa**

El router principal importa los prompts para combinarlos con chains LCEL.

---

### **A MODO DE EJEMPLO**

```python
from langchain_core.prompts import PromptTemplate

classifier_prompt = PromptTemplate.from_template("""
Clasifica la siguiente pregunta en una de las siguientes categorías:

- general → preguntas abiertas, explicaciones, creatividad, conversación normal.
- rag → preguntas que requieren usar información REAL proveniente de documentos, base de conocimiento o datos externos. Palabras clave: "basado en documentación", "según el textos almacenados", "extrae de información almacenada", "basado en el material", "qué indican los datos almacenados".
- summary → cuando se pide RESUMIR un texto proporcionado por el usuario. Solo se clasifica como summary si el usuario claramente proporciona texto para ser resumido.
- code → preguntas relacionadas con programación, errores, generación de funciones, fragmentos de código, debugging.
- math → problemas matemáticos, cálculos, expresiones numéricas, ecuaciones o razonamiento matemático.

Reglas importantes:
1. Si la pregunta pide resumir contenido proporcionado por el usuario → summary.
2. Si la pregunta pide extraer, buscar o consultar información de un documento, PDF, manual o contexto → rag.
3. Si no está claro que es summary o rag → clasificar como general.
4. Responde SOLO con una palabra EXACTA de esta lista:
general, rag, summary, code, math

Pregunta: "{input}"

Tu respuesta:
""")


general_prompt = PromptTemplate.from_template("""
Responde de forma clara y precisa, evitando información inventada o no verificada, si no tienes la respuesta di "No lo sé":
{input}
""")

code_prompt = PromptTemplate.from_template("""
Eres un asistente experto en Python. Ayuda al usuario con su código:
{input}
""")

summary_prompt = PromptTemplate.from_template("""
Resume el siguiente contenido de manera clara:
{input}
""")

math_prompt = PromptTemplate.from_template("""
Resuelve el siguiente ejercicio paso a paso, pero devuelve solo el resultado final:
{input}
""")

rag_prompt = PromptTemplate.from_template("""
Eres un asistente especializado en RAG. Debes responder **únicamente** con la información que aparezca en el siguiente contexto. 
No inventes datos, no agregues conocimiento externo y no uses información general que no esté contenida explícitamente en el contexto.

Si el contexto no contiene información suficiente para responder la pregunta, responde exactamente:
"Sin suficiente información en la documentación para responder."

Produce una respuesta:
- Clara, concisa y directa.
- Basada solo en detalles presentes en el contexto.
- Sintetizando y explicando, no copiando el contexto textual sin procesarlo.
- Sin añadir interpretaciones no justificadas por el contenido.

Contexto recuperado:
{context}

Pregunta:
{input}

Respuesta:
""")


```

---

## ✅ **4. `rag.py` — Pipeline RAG completo (Ejemplo real)**

### **Para qué sirve**

Este es **el corazón del mini-proyecto RAG**.

Incluye:

✔ Carga de documentos
✔ Web scraping
✔ Chunking
✔ Evita duplicados
✔ Inserta en ChromaDB
✔ Recuperación semántica
✔ Compresión contextual
✔ Envío al modelo → respuesta final

### **Cómo se usa**

El router llama:

```python
await answer_query(question)
```

Y el pipeline hace todo.

---

### **A MODO DE EJEMPLO**

```python
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

```

---

## ✅ **5. `loader.py` — Cargar y fragmentar documentos (Ejemplo real)**

### **Para qué sirve**

Carga todos los TXT y MD desde la carpeta `data/` y los divide en chunks.

### **Cómo se usa**

`rag.py` lo llama dentro de `build_vectorstore()`.

---

### **A MODO DE EJEMPLO**

```python
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

```

---

## ✅ **6. `chroma_client.py` — Cliente persistente ChromaDB**

### **Para qué sirve**

Crea un cliente persistente en disco y una colección.

### **Cómo se usa**

`rag.py` lo importa como:

```python
from .chroma_client import collection
```

---

### **A MODO DE EJEMPLO**

```python
import chromadb
from .config import COLLECTION_NAME, CHROMA_PATH

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)

```

---

## ✅ **7. `router.py` — Endpoint FastAPI del mini-proyecto RAG**

### **Para qué sirve**

Define:

* ruta `/query`
* esquema de entrada y salida
* indexado automático en background

### **Cómo se usa**

FastAPI lo monta en `main.py`.

---

### **A MODO DE EJEMPLO**

```python
import threading
from fastapi import APIRouter
from .config import URLS_TO_SCRAPE
from .schemas import QueryRequest, QueryResponse, SourceDocument
from .rag import build_vectorstore, answer_query

router = APIRouter(prefix="/a4v2", tags=["A4 - RAG Avanzado con web scraping, compresión contextual y fuentes puntuadas"])

# Lanzamos indexado en segundo plano al importar el router
def _auto_build_index():
    try:
        print("Construyendo índice RAG avanzado en background...")
        build_vectorstore(URLS_TO_SCRAPE)
        print("Índice RAG avanzado listo.")
    except Exception as e:
        print(f"[RAG] Error durante el indexado automático: {e}")

threading.Thread(target=_auto_build_index, daemon=True).start()


@router.post(
    "/query",
    summary="RAG Avanzado con web scraping, compresión contextual y fuentes puntuadas",
    description="""
    Implementar un pipeline **RAG completo** usando **LangChain**, con:
    - Carga automática de documentos locales.
    - Web scraping de URLs especificadas.
    - Compresión contextual.
    - Chunking inteligente.
    - Indexación persistente con **ChromaDB**.
    - Recuperación semántica.
    - Generación de respuestas con contexto real.
    """,
    response_description="Respuesta generada y documentos fuente",
    response_model=QueryResponse
)
async def query_rag(req: QueryRequest):
    result = await answer_query(req.question)
    # Formatear las fuentes según el esquema Pydantic
    formatted_sources = [SourceDocument(**src) for src in result["sources"]]
    return QueryResponse(
        answer=result["answer"],
        sources=formatted_sources,
    )

```

---

## ✅ **8. `scraper.py` — Web Scraper HTML**

### **Para qué sirve**

Hace scraping:

* limpia scripts/style
* extrae texto visible
* lo devuelve como `Document`

### **Cómo se usa**

`rag.py` lo usa dentro de `build_vectorstore()` cuando hay URLs.

---

### **A MODO DE EJEMPLO**

```python
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

# Función para scrapear una página web y devolver su contenido como lista de Document
def scrape_webpage(url: str) -> list[Document]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }
    
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    # Parseamos el contenido HTML, soup contiene el árbol DOM completo
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extraemos texto visible, obtenemos los tags no deseados y los eliminamos de soup
    # tag representa cada etiqueta no deseada encontrada y es un apuntador a la misma en el árbol DOM que contiene soup
    # tag no es un objeto independiente, por lo que al eliminarlo de soup, se elimina del árbol DOM original
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose() # Elimina etiquetas no deseadas

    # Obtenemos el texto limpio del árbol DOM modificado
    # retorna texto del dom sin tags HTML y separado por saltos de línea
    text = soup.get_text(separator="\n")
    # retorna una lista de líneas limpias sin espacios en blanco ni líneas vacías
    clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
    # unimos las líneas limpias en un solo string separado por saltos de línea
    clean_text = "\n".join(clean_lines)

    # Retornamos el contenido como una lista con un solo Document
    return [Document(page_content=clean_text, metadata={"source": url})]

```

---

## ✅ **9. `utils.py` — Utilidades reusables**

### **Para qué sirve**

Funciones clave del pipeline:

* **hash_text** → evita duplicados
* **is_chunk_indexed** → consulta Chroma
* **format_sources** → genera puntuación de similitud

### **Cómo se usa**

`rag.py` importa todas estas utilidades.

---

### **A MODO DE EJEMPLO**

```python
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

```

---
