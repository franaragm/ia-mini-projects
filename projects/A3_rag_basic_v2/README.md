# 🧠 Proyecto A3v2 – RAG Básico Mejorado (indexado automático en segundo plano)

## 📘 Descripción general

Este mini proyecto implementa un sistema **RAG (Retrieval-Augmented Generation)** básico pero optimizado, que permite responder preguntas del usuario **basándose en documentos locales indexados automáticamente** mediante embeddings.

A diferencia de la versión anterior (`A3_rag_basic`), esta versión:

* 🧩 **Indexa los documentos automáticamente al iniciar el servidor**.
* 🚀 Lo hace **en un hilo en segundo plano**, sin bloquear FastAPI.
* 📄 **Fragmenta los documentos** en trozos para mejorar la recuperación semántica.
* 💾 **Persiste los embeddings** con **ChromaDB**, evitando reindexar cada vez.
* ✅ Devuelve una **respuesta JSON estructurada**, con la respuesta y las fuentes utilizadas.


---

## 💡 Mejoras clave respecto a la versión A3 original

| Mejora                      | Descripción                                        |
| --------------------------- | -------------------------------------------------- |
| 🧠 Indexado automático      | Los documentos se indexan al iniciar FastAPI.      |
| 🚀 Hilo en segundo plano    | El servidor no se bloquea durante el indexado.     |
| 🧩 Fragmentación automática | Divide textos largos en bloques de 400 caracteres. |
| 🔐 Evita duplicados         | Detecta contenido repetido mediante hash.          |
| 💾 Persistencia local       | Guarda los embeddings en `./chroma_db`.            |
| ✅ Respuesta JSON limpia     | Respuesta estructurada con `answer` y `sources`.   |

---
