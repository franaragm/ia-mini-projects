# **A5 – LangChain Chains & Routers**

Cadenas secuenciales, cadenas de transformación y enroutamiento dinámico

Este proyecto extenderá la arquitectura existente e introducirá:

---

# ✅ **Objetivos del mini-proyecto A5**

### 1) **Crear cadenas (Chains) para construir aplicaciones más complejas**

Aprenderemos a usar `LLMChain`, `SequentialChain`, `TransformChain`, etc.

### 2) **Crear un modelo secuencial que combine cadenas**

Ejemplo:
**Pregunta → Clasificación → Reformulación → Búsqueda → Respuesta final**

### 3) **Enrutar dinámicamente a la mejor cadena**

Con `MultiPromptChain` o `RouterChain` basado en intención.

### 4) **Crear cadenas avanzadas de transformación + QA sobre vectorstore**

Pipeline completo combinando:

* Transformaciones previas
* RAG sobre ChromaDB
* Compresión
* Respuesta final

---

# 📁 Estructura que añadiremos al repositorio

Siguiendo tu convención:

```
projects/
├── A1_chat_structured/
├── A2_output_parser/
├── A3_rag_basic/
├── A3_rag_basic_v2/
├── A4_rag_advanced/
├── A4_rag_advanced_v2/
└── A5_chains_and_routers/
    ├── router.py
    ├── chains.py
    ├── prompts.py
    ├── schemas.py
    ├── rag_logic.py
    └── README.md
```

Y agregaremos:

```python
from projects.A5_chains_and_routers.router import router as a5_router
router.include_router(a5_router)
```

---

# 📘 **DISEÑO DEL MINI PROYECTO A5**

A5 demostrará:

---

## **🔹 1. Cadena de Clasificación (`ClassifierChain`)**

Determinará la intención de la pregunta:

* “pregunta general”
* “pregunta sobre código”
* “pregunta que requiere búsqueda RAG”
* “pregunta que requiere resumen”
* “pregunta matemática”

---

## **🔹 2. TransformChain**

Ejemplo: Normalizar texto → convertir a forma corta → filtro de toxicidad (sintético).

---

## **🔹 3. RAGChain**

Reutilizaremos ChromaDB, pero ahora como parte de una *cadena* de LangChain.

---

## **🔹 4. RouterChain (¡estrella del proyecto!)**

Enrutará a:

* **GeneralAnswerChain**
* **CodeHelperChain**
* **RagChain**
* **SummarizerChain**
* **MathChain**

Cada una es un `LLMChain`.

---

## **🔹 5. SequentialChain final**

Pipeline:

```
Input → Clasificación → Enrutamiento → Ejecución de la cadena seleccionada → Respuesta final
```

---

# 🎯 Router final esperado

Ejemplo de comportamiento:

| Entrada del usuario                                        | Chain seleccionada |
| ---------------------------------------------------------- | ------------------ |
| “Explica qué es FastAPI”                                   | GeneralChain       |
| “Aquí está mi código, no funciona…”                        | CodeHelperChain    |
| “Según los documentos del proyecto, ¿qué es un embedding?” | RagChain           |
| “Resume este artículo”                                     | SummaryChain       |
| “6 × 11 + 4”                                               | MathChain          |

---

