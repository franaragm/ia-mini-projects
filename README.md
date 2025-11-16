# Mini Proyectos Laboratorio: LangChain — Servidor IA en Python

Este repositorio contiene una serie de **mini-proyectos progresivos** diseñados para aprender a construir sistemas de **IA aplicados a software real**, usando:

| Tecnología            | Para qué se usa                                                    |
| --------------------- | ------------------------------------------------------------------ |
| **Python**            | Lenguaje principal del servidor IA                                 |
| **FastAPI**           | Crear endpoints HTTP que devuelven JSON                            |
| **LangChain**         | Orquestar modelos de lenguaje, prompts, RAG y agentes              |
| **OpenRouter**        | Acceder a modelos avanzados (Mistral, Gemini, LLaMA, Claude, etc.) |
| **Embeddings**        | Representar texto como vectores para búsqueda semántica            |
| **ChromaDB / Qdrant** | Bases de datos vectoriales para RAG                                |

---

## 🎯 Objetivo del repositorio

Aprender paso a paso a:

* Controlar y estructurar la salida de un modelo de lenguaje (sin inventos)
* Validar y tipar respuestas (`OutputParser`)
* Crear un sistema RAG (consultas basadas en documentos reales)
* Mitigar alucinaciones y justificar respuestas
* Darle **herramientas** a la IA (agentes que ejecutan funciones)
* Conectar la IA con **APIs externas** (ej: Uptask → más adelante)

Cada mini-proyecto se construye **uno encima del anterior**, pero todos están organizados en carpetas independientes.

---

## 🏗️ Estructura del repositorio

```
mini-projects-langchain/
│
├─ README.md          # Este documento
├─ .env.example       # Variables de entorno a copiar
├─ requirements.txt   # Dependencias compartidas
├─ app/               # Código común (FastAPI base + cliente LLM + utilidades)
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
    ├─ A5_tools_basic/
    └─ A6_tools_external_api/
```

### Sobre el directorio `app/`

`/app` contiene **código base compartido** entre mini-proyectos:

* Inicialización de **FastAPI**
* Cliente para llamar modelos en **OpenRouter**
* Helpers que se reutilizan

Cada mini-proyecto solo **extiende o monta nuevas rutas**.

---

## 🧠 Lista de Mini Proyectos (A1 → A6)

| Mini Proyecto                        | Qué aprenderás                                    | Resultado                                   |
| ------------------------------------ | ------------------------------------------------- | ------------------------------------------- |
| **A1. Chat estructurado**            | Controlar el tono y formato                       | IA responde siguiendo un prompt fijo        |
| **A2. Output Parser**                | Validar y tipar respuestas                        | IA devuelve JSON correcto y útil            |
| **A3. RAG básico**                   | Cargar & dividir documentos, embeddings, búsqueda | IA usa conocimiento real sin inventar       |
| **A3. RAG básico V2**                | Cargar & dividir documentos, embeddings, búsqueda | IA usa conocimiento real sin inventar       |
| **A4. RAG avanzado**                 | Anti-alucinaciones (score, top-k, evidencia)      | IA justifica sus respuestas                 |
| **A5. Tools / Agentes**              | Dar habilidades a la IA                           | IA puede ejecutar funciones automáticamente |
| **A6. API externa como herramienta** | Integración IA ↔ servicios externos               | IA consulta datos reales desde web/API      |

Cada carpeta contiene:

```
- README.md (explicación detallada)
- Código paso a paso
- Ejercicios
- Pruebas con cURL / Thunder Client
```

---

## ⚙️ Instalación del entorno

### 1) Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate      # mac / linux
.venv\Scripts\activate         # windows
```

### 2) Instalar dependencias

```bash
pip install --upgrade pip # opcional
pip install -r requirements.txt
```

### 3) Configurar `.env`

Crea tu archivo desde la plantilla:

```bash
cp .env.example .env
```

Edita OPENROUTER_API_KEY:

Puedes editar también DEFAULT_MODEL si deseas usar otro modelo de OpenRouter.

```
OPENROUTER_API_KEY=API_KEY_HERE
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
DEFAULT_MODEL=meta-llama/llama-3.3-8b-instruct:free
```

> La API key se obtiene en: [https://openrouter.ai/keys](https://openrouter.ai/keys)

---

## ▶️ Ejecutar el servidor desde entorno virtual

```bash
uvicorn app.main:app --reload --port 8000
```

Probamos:

```
GET http://localhost:8000/health
GET http://localhost:8000/test-llm
```

---


¡Perfecto! Aquí tienes un **apartado completo y muy claro**, detallando **pyenv, configuración de shell, entorno virtual, pip y dependencias sin caché**, listo para incluir en tu README para este equipo macOS Intel:

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

Si quieres, puedo hacer una **versión resumida “nota rápida del equipo”**, de unas 10-12 líneas, perfecta para poner **al final del README** y que quede claro para cualquier persona que use este Mac Intel.

¿Quieres que haga eso?

