# 🚀 **A5 – LangChain LCEL: Chains, Runnables y Router Inteligente**

Este módulo implementa un pipeline profesional basado en **LangChain Expression Language (LCEL)** para:

* Crear *chains declarativas y componibles*
* Enrutar preguntas a la cadena correcta mediante clasificadores
* Combinar *async* + *sync*
* Usar `RunnableBranch`, `RunnableLambda`, `RunnablePassthrough`
* Integrar RAG como chain LCEL sin funciones externas

El archivo clave del proyecto es:

```
A5_chains_routers/
│
├── chains.py  ← ⭐ EXPLICADO A DETALLE EN ESTE README
├── router.py
├── prompts.py
├── rag.py   ← solo contiene retrieve_context()
└── ...
```

---

# 📘 **1. Overview del flujo completo**

El pipeline final aplica esta secuencia:

```
Pregunta
   ↓
ClassifierChain  (LCEL)
   ↓  intent: rag | code | summary | math | general
RouterChain (RunnableBranch)
   ↓
Cadena seleccionada (General/Code/Summary/Math/RAG)
   ↓
Respuesta final + chain_used
```

Diagrama:

```
                   ┌──────────────────┐
                   │ classifier_chain │
                   └─────────┬────────┘
                             │  intent
                             ▼
┌──────────────────────────────────────────────────┐
│                 router_chain                     │
│ (RunnableBranch con condiciones dinámicas)       │
├──────────────────────────────────────────────────┤
│ "rag"     → rag_chain                            │
│ "code"    → code_chain                           │
│ "summary" → summary_chain                        │
│ "math"    → math_chain                           │
│ default   → general_chain                        │
└──────────────────────────────────────────────────┘
                             │
                             ▼
                   Respuesta final
```

---

# 🧠 **2. ¿Qué es LCEL y por qué se usa aquí?**

**LCEL (LangChain Expression Language)** permite componer chains usando operadores:

* `|` pipe operator: *encadena steps*
* Runnables como:

  * `RunnableLambda` → transforma inputs/outputs con Python puro
  * `RunnableBranch` → router inteligente
  * `RunnablePassthrough` → paso de datos sin modificar

Ventajas:

* Declarativo
* Menos boilerplate
* Funciona igual en sync + async
* Mejor rendimiento (streaming optimizado)

---

# 📂 **3. Explicación línea por línea de `chains.py`**

---

## 🔸 **Imports**

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough
from app.services.llm_client import llm_chain
from .prompts import (
    classifier_prompt,
    general_prompt,
    code_prompt,
    summary_prompt,
    math_prompt,
    rag_prompt,
)
from .rag import retrieve_context
```

### Explicación

* `StrOutputParser` → Normaliza la salida del LLM como un string limpio.
* `RunnableBranch` → Router condicional.
* `RunnableLambda` → Funciones Python dentro de una cadena.
* `RunnablePassthrough` → paso de datos sin transformación.
* `llm_chain()` → Devuelve el cliente LLM (OpenRouter, OpenAI, etc.).
* `prompts.py` → Cada chain tiene su prompt.
* `retrieve_context()` → Solo recuperación de contexto para RAG.

---

# 🧱 **4. Inicializar LLM + Parser**

```python
llm = llm_chain()
parser = StrOutputParser()
```

---

# 🏗️ **5. Creación de cada chain con LCEL**

Cada chain sigue el patrón:

```
prompt → llm → parser → formateo final (RunnableLambda)
```

Ejemplo:

```python
general_chain = (
    general_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "general_chain"})
)
```

---

## 🔹 **RAG Chain totalmente LCEL**

Ahora el RAG se construye como un **pipeline declarativo**:

```python
rag_chain = (
    {"input": RunnablePassthrough()}  # Paso la pregunta
    | RunnableLambda(lambda x: {
        "input": x["input"],
        "context": retrieve_context(x["input"])
    })  # Recupera contexto
    | RunnableLambda(lambda x: rag_prompt.format(
        context=x["context"],
        input=x["input"]
    ))  # Construye prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "rag_chain"})
)
```

**Ventajas**:

* No se necesita función async externa
* Encapsula todo: recuperación + prompt + LLM + parseo
* Siempre devuelve `{answer, chain_used}`

---

# 🚦 **6. Router LCEL (RunnableBranch)**

```python
router_chain = RunnableBranch(
    (lambda x: "rag" in x["intent"], rag_chain),
    (lambda x: "code" in x["intent"], code_chain),
    (lambda x: "summary" in x["intent"], summary_chain),
    (lambda x: "math" in x["intent"], math_chain),
    general_chain,  # default
)
```

---

# ⚙️ **7. Función principal: `run_router_chain()`**

```python
async def run_router_chain(question: str):
    intent = classifier_chain.invoke({"input": question}).strip().lower()
    block = await router_chain.ainvoke({"intent": intent, "input": question})
    return {
        "intent": intent,
        "chain_used": block["chain_used"],
        "answer": block["answer"].strip(),
    }
```

---

# 🏁 **8. Resultados**

Cada llamada devuelve un diccionario uniforme:

```json
{
  "intent": "summary",
  "chain_used": "summary_chain",
  "answer": "Texto resumido..."
}
```

---

# 🎯 **9. Cambios clave respecto a versiones previas**

* `rag_chain` ahora **LCEL**, no función async en rag.py
* `rag.py` solo conserva `retrieve_context()`
* Uso de `RunnablePassthrough` y `RunnableLambda` para un pipeline 100% declarativo
* Router con `RunnableBranch` profesional
* Formato de salida unificado en todas las chains

---

# ✔️ **10. Cómo extender el sistema**

1. Crear prompt nuevo en `prompts.py`
2. Declarar la chain usando `| llm | parser | RunnableLambda`
3. Añadir condición en `router_chain`


---
