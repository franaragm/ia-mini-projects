# 🚀 **A5 – LangChain LCEL: Chains, Runnables y Router Inteligente**

Este módulo implementa un pipeline profesional basado en **LangChain Expression Language (LCEL)** para:

* Crear *chains declarativas y componibles*
* Enrutar preguntas a la cadena correcta mediante clasificadores
* Combinar *async* + *sync*
* Usar `RunnableBranch`, `RunnableLambda`, `RunnableMap`
* Encapsular un RAG como chain integrada

El archivo clave del proyecto es:

```
A5_chains_routers/
│
├── chains.py  ← ⭐ EXPLICADO A DETALLE EN ESTE README
├── router.py
├── prompts.py
├── rag.py
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
  * `RunnableMap` → salida estructurada

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
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
)
from app.services.llm_client import llm_chain
from .prompts import (
    classifier_prompt,
    general_prompt,
    code_prompt,
    summary_prompt,
    math_prompt,
)
from .rag import rag_chain
```

### Explicación

* `StrOutputParser` → Normaliza la salida del LLM como un string limpio.
* `RunnableBranch` → Router condicional “si X entonces usa esta chain”.
* `RunnableLambda` → Funciones Python dentro de una cadena.
* `llm_chain()` → Devuelve el cliente LLM (OpenAI, OpenRouter, etc.).
* `prompts.py` → Cada chain tiene su prompt.
* `rag_chain` → RAG declarado como runnable independiente.

---

# 🧱 **4. Inicializar LLM + Parser**

```python
llm = llm_chain()
parser = StrOutputParser()
```

### Explicación

* `llm` es un runnable — cualquier chain puede recibirlo vía `|`.
* `parser` convierte la respuesta del LLM en texto sin formato.

---

# 🏗️ **5. Creación de cada chain con LCEL**

Cada chain sigue este patrón:

```
prompt → llm → parser → formateo final (RunnableLambda)
```

Ejemplo completo:

---

## 🔹 **General Chain**

```python
general_chain = (
    general_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "general_chain"})
)
```

### Explicación **línea por línea**

#### `general_prompt | llm`

Envía el prompt al modelo y obtiene respuesta cruda.

#### `| parser`

Convierte la salida del modelo a un string limpio.

#### `| RunnableLambda(lambda x: {...})`

**Añade metadatos adicionales** a la salida.

### 🔍 ¿Qué hace exactamente el `lambda`?

La firma es:

```python
lambda x: {"answer": x, "chain_used": "general_chain"}
```

Esto significa:

* Recibe la salida del paso anterior (`x = respuesta del LLM`)
* Produce un diccionario nuevo con:

  * `"answer"`     → texto de la respuesta
  * `"chain_used"` → nombre de la chain

Así todas las chains devuelven el mismo esquema.

---

## 🔹 **Otras Chains (idéntico patrón)**

Todas siguen el mismo diseño:

```python
code_chain = (
    code_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "code_chain"})
)

summary_chain = (
    summary_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "summary_chain"})
)

math_chain = (
    math_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "math_chain"})
)
```

---

## 🔹 **RAG Chain**

```python
rag_chain = (
    rag_chain
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "rag_chain"})
)
```

---

# 🚦 **6. Construcción del Router LCEL (RunnableBranch)**

Este es el corazón del sistema.

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

## 🧩 Cómo funciona `RunnableBranch`

`RunnableBranch` evalúa cada condición en orden:

```
(condición1, cadena1)
(condición2, cadena2)
...
default_chain
```

El primer condicional `True` determina la chain seleccionada.

---

## 🔍 Explicación de cada `lambda`

Ejemplo:

```python
lambda x: "rag" in x["intent"]
```

Significa:

* Recibe un diccionario `x` con:

  ```json
  {"intent": "<intención>", "input": "<pregunta>"}
  ```
* Evalúa si la intención contiene `"rag"`.

Si es True → se ejecuta `rag_chain`.

---

### 🔥 Diagrama del router

```
                 intent
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
   (lambda cond1)        ¿True? sí → rag_chain
         │ no
         ▼
   (lambda cond2)        ¿True? sí → code_chain
         │ no
         ▼
   (lambda cond3)        ¿True? sí → summary_chain
         │ no
         ▼
   (lambda cond4)        ¿True? sí → math_chain
         │ no
         ▼
       default → general_chain
```

---

# ⚙️ **7. Función principal: `run_router_chain()`**

```python
async def run_router_chain(question: str):

    # Paso 1: Intent
    intent = classifier_chain.invoke({"input": question}).strip().lower()

    # Paso 2: Router async
    block = await router_chain.ainvoke({"intent": intent, "input": question})

    # Paso 3: Resultado final
    return {
        "intent": intent,
        "chain_used": block["chain_used"],
        "answer": block["answer"].strip(),
    }
```

## Explicación paso a paso

---

### **1) Clasificación (sync)**

```python
intent = classifier_chain.invoke({"input": question})
```

* `invoke()` es SÍNCRONO.
* Devuelve string.
* Se normaliza `.strip().lower()`.

---

### **2) Router (async)**

```python
block = await router_chain.ainvoke(...)
```

* `ainvoke()` es *asíncrono*.
* `router_chain` decide la chain que se ejecuta mediante `RunnableBranch`.
* `block` contiene:

  ```json
  {
    "answer": "...",
    "chain_used": "summary_chain"
  }
  ```

---

### **3) Respuesta estructurada**

```python
return {
    "intent": intent,
    "chain_used": block["chain_used"],
    "answer": block["answer"].strip(),
}
```

---

# ✔️ **8. Resultado final del pipeline**

Cuando llamas a:

```python
await run_router_chain("resume este texto...")
```

El sistema sigue este flujo:

```
input
 ↓
classifier_chain.invoke()
 ↓ intent="summary"
router_chain.ainvoke()
 ↓
summary_chain
 ↓
{ "answer": "...", "chain_used": "summary_chain" }
```

---

# 🎯 **9. Ventajas de esta arquitectura**

| Elemento             | Función                                        |                                 |
| -------------------- | ---------------------------------------------- | ------------------------------- |
| **LCEL               | **                                             | Composición clara y declarativa |
| **RunnableLambda**   | Adjuntar metadata & transformar outputs        |                                 |
| **RunnableBranch**   | Enrutamiento profesional                       |                                 |
| **Async + Sync**     | Compatible con FastAPI                         |                                 |
| **Formato uniforme** | Todas las chains devuelven la misma estructura |                                 |

---

# 🏁 **10. Conclusión**

Este proyecto demuestra cómo construir un **router inteligente modular**, con una arquitectura clara, mantenible y extensible basada en LangChain LCEL.

Puedes añadir nuevas chains simplemente:

1. Crear prompt
2. Declarar chain con `| llm | parser | RunnableLambda`
3. Añadir condición al router

Escalable y 100% profesional.

---
