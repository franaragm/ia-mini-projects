# Mini Proyecto A3: RAG Básico

## Objetivo

El objetivo de este mini proyecto es implementar un **RAG (Retrieval-Augmented Generation) básico**.  
Esto significa que vamos a:

- Indexar documentos locales (TXT, PDF, Markdown) usando **embeddings**.
- Almacenar los vectores en una **base de datos vectorial local** (ChromaDB).
- Recuperar documentos relevantes ante una consulta de usuario.
- Integrar estos documentos como contexto para un LLM (OpenRouter) y generar respuestas más precisas, reduciendo las alucinaciones.

Con este mini proyecto aprenderás:

- Cómo usar **Sentence Transformers** para crear embeddings.
- Cómo usar **ChromaDB** para almacenamiento y búsqueda semántica.
- La base del **RAG**: recuperar información relevante antes de generar texto.

---

## Estructura del proyecto

````

A3_rag_basic/
├─ router.py        # Endpoint FastAPI para consultar documentos
├─ rag.py           # Lógica de embeddings, indexación y recuperación
├─ schemas.py       # Esquemas de entrada y salida para FastAPI
├─ prompts.py       # Prompt templates para LLM
├─ loader.py        # Carga documentos de un path     
├─ data/            # Documentos de prueba (TXT/MD)
└─ README.md

````

---

## Detalles técnicos

* **rag.py**:

  * `SentenceTransformer("all-MiniLM-L6-v2")` → crea embeddings de texto.
  * `ChromaDB` → almacena y consulta vectores.
  * `build_index(documents)` → indexa documentos.
  * `retrieve(question)` → devuelve los documentos más relevantes.
  
* **router.py**:

  * Define el endpoint FastAPI `/a3/query`.
  * Llama a `retrieve(question)` y genera respuesta usando LLM.
  
* **prompts.py**:

  * Prompt template para indicar al LLM que use la información recuperada como contexto.

---
