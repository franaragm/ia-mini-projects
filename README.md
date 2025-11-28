# **Mini Proyectos Laboratorio: LangChain — Servidor IA en Python**

Este repositorio contiene una serie de **mini-proyectos progresivos** diseñados para aprender a construir sistemas de **IA aplicados a software real**, usando herramientas modernas del ecosistema LLM:

| Tecnología               | Para qué se usa                                                    |
| ------------------------ | ------------------------------------------------------------------ |
| **Python**               | Lenguaje principal del servidor IA                                 |
| **FastAPI**              | Crear endpoints HTTP que devuelven JSON                            |
| **LangChain**            | Orquestar modelos de lenguaje, prompts, chains, RAG y agentes      |
| **OpenRouter**           | Acceder a modelos avanzados (Mistral, Gemini, LLaMA, Claude, etc.) |
| **Embeddings**           | Representar texto como vectores para búsqueda semántica            |
| **ChromaDB**             | Base vectorial persistente para sistemas RAG                       |
| **SentenceTransformers** | Generar embeddings locales                                         |

---

## 🎯 Objetivos del repositorio

El propósito de estos mini-proyectos es aprender a construir **aplicaciones AI reales**, avanzando desde prompts simples hasta arquitecturas completas con RAG, agentes y routers.

Aprenderás a:

### 🧩 Control del modelo

* Controlar y estructurar la salida de un modelo de lenguaje
* Validar y tipar respuestas (**OutputParser**)
* Encadenar pasos de razonamiento y transformar texto

### 📚 RAG (Retrieval Augmented Generation)

* Crear pipelines RAG básicos y avanzados
* Cargar, dividir y vectorizar documentos
* Construir y persistir bases de datos vectoriales
* Recuperar información con precision (top-k, puntajes, compresión contextual)
* Integrar web scraping en el pipeline RAG

### 🧠 Agentes y Herramientas

* Dar herramientas reales a un LLM
* Ejecutar funciones automáticamente desde la IA
* Conectar la IA con APIs externas
* Gestionar memoria y contexto entre llamadas

### 🧵 Chains (A5)

* Crear **cadenas secuenciales** para combinar modelos
* Crear cadenas de **transformación**
* Crear **Router Chains** para enrutar dinámicamente
* Combinar **RAG + Chains + Clasificación de intención**
* Construir pipelines complejos estilo:

  ```
  Pregunta → Clasificador → Transformadores → RAG → LLM → Respuesta final
  ```

---

## 🏗️ Estructura del repositorio

```
mini-projects-langchain/
│
├─ README.md
├─ config_base.py        # Configuración global compartida
├─ .env.example
├─ requirements.txt
│
├─ app/
│   ├─ main.py
│   ├─ routes.py
│   └─ services/
│       ├─ llm_client.py
│       └─ utils.py
│
└─ projects/
    ├─ A1_chat_structured/
    ├─ A2_output_parser/
    ├─ A3_rag_basic/
    ├─ A3_rag_basic_v2/
    ├─ A4_rag_advanced/
    ├─ A4_rag_advanced_v2/
    ├─ A5_chains_and_routers/
    ├─ A5_tools_basic/
    └─ A6_tools_external_api/

```

### Sobre el directorio `app/`

`/app` contiene **todos los componentes base compartidos**:

* Inicialización de **FastAPI**
* Enrutador general del servidor
* Cliente universal para LLM vía **OpenRouter**
* Archivos de configuración global
* Utilidades para cargar variables de entorno

Cada mini-proyecto solo agrega una nueva ruta o endpoint mediante:

```python
router.include_router(aX_router)
```

---

## 🧠 Lista de Mini Proyectos Completos

### **A1 — Chat estructurado**

* Prompt fijo
* Respuesta controlada

### **A2 — Output Parser**

* Validación estricta
* Tipado de salida
* Conversión a JSON robusto

### **A3 — RAG Básico**

* Cargar documentos
* Fragmentarlos
* Crear embeddings
* Recuperar contexto

### **A3 V2 — RAG Básico Mejorado**

* Limpieza mejorada
* Separadores custom
* Mejor chunking

### **A4 — RAG Avanzado**

* Evidencias
* Fuentes con puntaje
* Control anti-alucinaciones

### **A4 V2 — RAG con Web Scraping + Compresión Contextual**

* Scrapeo de páginas web
* Mezclar documentos locales y online
* Compresión del contexto
* RAG de múltiples etapas

---

## 🆕 **A5 — Chains & Routers (Cadenas avanzadas)**

Este mini-proyecto es una expansión importante. Incluye:

### ✔️ Clasificador de intención (Intent Classifier)

Determina si la pregunta es:

* general
* sobre código
* RAG
* resumen
* matemática

### ✔️ Cadenas específicas (General, Code, Summary, Math)

Cada cadena es un **LLMChain**.

### ✔️ RAGChain integrada

Integración directa con ChromaDB para consultas semánticas dentro de una chain.

### ✔️ Router dinámico

Lógica para enrutar la petición hacia la chain correcta:

```
Input → ClassifierChain → [GeneralChain | CodeChain | SummaryChain | MathChain | RAGChain]
```

### ✔️ Cadena secuencial avanzada

Permite construir aplicaciones complejas combinando pasos:

```
→ Normalizar texto
→ Clasificar intención
→ Seleccionar cadena
→ Ejecutar pipeline RAG si aplica
→ Generar respuesta final
```

Este mini-proyecto introduce **la arquitectura que usan aplicaciones reales** (Copilot, ChatGPT Tools, agentes planificadores, etc.).

---

## ⚙️ Instalación del entorno

### 1) Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

### 2) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3) Configurar variables de entorno

```bash
cp .env.example .env
```

Edita tu `.env`:

```
OPENROUTER_API_KEY=TU_API_KEY
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
ENV=dev
```

Obtener API key:
[https://openrouter.ai/keys](https://openrouter.ai/keys)

---

## ▶️ Ejecutar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

Rutas de prueba:

```
GET /health
GET /test-llm
```

---


## 🛠️ **config_base.py (configuración global del repositorio)**

Este archivo centraliza la configuración compartida entre todos los mini-proyectos.

Se encuentra en:

```
/config_base.py
```

### ✔️ ¿Por qué existe este archivo?

Evita repetición de lógica en cada mini-proyecto:

* Define rutas absolutas comunes
* Establece los modelos LLM por defecto
* Define el modelo de embeddings estándar
* Mantiene la configuración de almacenamiento del RAG centralizada

Así cualquier mini-proyecto puede simplemente importar:

```python
from config_base import CHROMA_PATH, DEFAULT_LLM_MODEL
```

---

## 📄 **Contenido completo de `config_base.py`**

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

## 🚀 ¿Qué sigue?

Puedes continuar con:

* **A6: Tools con APIs externas reales**
* **A7: Memory, historiales y buffers**
* **A8: Agents con múltiples herramientas**
* **A9: Multi-step planning (ReAct / MRKL)**
* **A10: RAG híbrido (web + local + embeddings mixtos)**

---

## ⚠️ Consideraciones para macOS Intel (Python 3.11)

En este equipo específico con macOS 14 Intel, se requieren algunos pasos adicionales para evitar conflictos de dependencias:

---

### 1️⃣ Instalar pyenv y configurar Python 3.11

1. Instalamos `pyenv`:

```bash
brew install pyenv
```

2. Instalamos Python 3.11 y lo configuramos como **versión global** del equipo:

```bash
pyenv install 3.11.8
pyenv global 3.11.8
```

3. Verificamos que se use la versión correcta:

```bash
python3 -V       # Debe mostrar Python 3.11.8
which python3    # Debe apuntar a ~/.pyenv/versions/3.11.8/bin/python3
```

---

### 2️⃣ Configurar el shell (`zsh`) para pyenv

Para que pyenv funcione correctamente en todas las sesiones, añadimos estas líneas a **`~/.zshrc`** o **`~/.zprofile`**:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"
```

Luego recargamos la configuración:

```bash
source ~/.zshrc
```

> Esto asegura que `python3` y `pip` apunten a la versión de pyenv, no al Python del sistema.

---

### 3️⃣ Crear y activar entorno virtual

1. Creamos un entorno virtual dentro del proyecto:

```bash
python -m venv .venv
```

2. Activamos el entorno:

```bash
source .venv/bin/activate   # macOS / Linux
```

3. Verificamos que `python` y `pip` apunten al entorno virtual:

```bash
which python   # Debe apuntar a .venv/bin/python
which pip      # Debe apuntar a .venv/bin/pip
python -V      # Debe mostrar Python 3.11.8
```

---

### 4️⃣ Instalar pip para la versión de pyenv

Si el entorno no tiene pip:

```bash
python -m ensurepip
python -m pip install --upgrade pip
```

> Ahora pip está correctamente asociado a Python 3.11 del entorno virtual.

---

### 5️⃣ Forzar NumPy < 2

Para compatibilidad con paquetes compilados (PyTorch, sentence-transformers):

```bash
pip uninstall numpy -y
pip install "numpy<2"
```

---

### 6️⃣ Instalar dependencias sin usar caché

```bash
pip install --no-cache-dir -r requirements.txt
```

> Esto evita que se instalen versiones antiguas o incompatibles de los paquetes.

---

### 7️⃣ Verificar instalación

```bash
python -c "import numpy; print(numpy.__version__)"
python -c "import torch; print(torch.__version__)"
python -c "from sentence_transformers import SentenceTransformer; print('ST OK')"
```

Todo debe funcionar sin errores.

---

### 8️⃣ Arrancar el servidor

Con el entorno activado:

```bash
uvicorn app.main:app --reload --port 8000
```

> Ahora el servidor funciona correctamente, sin errores de NumPy o PyTorch en este equipo.

---

