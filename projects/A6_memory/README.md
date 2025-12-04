# A6 – Memory System (LangGraph + ChromaDB)

Este mini-proyecto implementa un **sistema de memoria conversacional** para asistentes basados en LLM, permitiendo:

* Guardar y consultar memoria por `user_id`
* Integrarse con un grafo conversacional creado con **LangGraph**
* Persistir información en **ChromaDB**
* Recuperar contexto relevante para mejorar respuestas
* Borrar memoria de un usuario cuando sea necesario

El objetivo es simular un asistente que **recuerda interacciones pasadas** y usa dicha información para responder mejor a nuevas consultas.

---

## Estructura principal

```

A6_memory/
│
├── router.py            # Endpoints FastAPI para consulta y gestión de memoria
├── config.py            # Configuración del nombre y path de ChromaDB
├── chroma_client.py     # Cliente persistente de ChromaDB
│
├── prompts.py           # Prompts para preparación y consulta de memoria
├── schemas.py           # Modelos Pydantic para el grafo y la API
├── llm_node.py          # Nodo principal: prepara memoria, llama al LLM, guarda resultados
├── memory_graph.py      # Grafo de LangGraph que define el flujo conversacional

````

---

## ¿Cómo funciona?

### 1️⃣ Consulta del usuario (endpoint `/query`)

El usuario envía:

```json
{
  "user_id": "user_123",
  "question": "¿Qué acordamos la última vez sobre el presupuesto?"
}
````

El proceso completo:

1. Se crea un estado inicial para el grafo (`messages`, `meta`, `user_id`).
2. El grafo ejecuta sus nodos en orden:

   * `add_user_message`
   * `maybe_summarize`
   * `call_llm`
3. El nodo `call_llm`:

   * Prepara la memoria del usuario mediante un LLM (`memory_preparation_prompt`) a partir de la última interacción.
   * Guarda la memoria estructurada en ChromaDB.
   * Recupera las memorias más recientes de ChromaDB para la respuesta.
   * Construye un prompt con **solo la información relevante para la pregunta actual** (`memory_prompt` optimizado).
   * Llama al LLM para generar la respuesta.
4. Se devuelve la respuesta generada + información sobre qué memoria se usó.

Ejemplo de respuesta:

```json
{
  "answer": "Acordamos que el presupuesto máximo sería de 500 USD.",
  "memory_used": ["summary", "buffer"]
}
```

---

## LangGraph: Flujo conversacional

El grafo está definido en `memory_graph.py`:

```
START
  ↓
add_user_message
  ↓
maybe_summarize
  ↓
call_llm
  ↓
END
```

✔ Mantiene un mini-summary de los últimos 10 mensajes
✔ Control simple y eficiente para proyectos pequeños
✔ Persistencia externa en ChromaDB (sin InMemorySaver)

---

## ChromaDB: Persistencia de memoria

* Cada fragmento de memoria se guarda como un documento separado.
* Identificado por `user_id`.
* Se añade automáticamente cada vez que el asistente procesa un mensaje.
* Consultado mediante búsquedas semánticas con `collection.query(...)`.

### Endpoints útiles

#### ✔ **Obtener memoria de un usuario**

`GET /a6memory/memory_state/{user_id}`

#### ✔ **Borrar memoria**

`POST /a6memory/clear/{user_id}`

---

## Endpoints del router

### `POST /a6memory/query`

Consulta el grafo y devuelve respuesta del asistente, usando memoria relevante.

### `GET /a6memory/memory_state/{user_id}`

Devuelve los documentos de memoria persistidos en ChromaDB.

### `POST /a6memory/clear/{user_id}`

Elimina toda la memoria de un usuario, borrando sus IDs en la colección.

---

## Lógica del nodo principal (`llm_node.py`)

El nodo:

1. Normaliza el estado del chat (dict o Pydantic).
2. Prepara la memoria relevante usando un LLM (`memory_preparation_prompt`) antes de guardarla.
3. Guarda la memoria limpia en ChromaDB.
4. Recupera la memoria más reciente del usuario.
5. Construye un prompt optimizado (`memory_prompt`) que **solo devuelve lo que se pregunta**, ignorando información irrelevante.
6. Llama al LLM para generar la respuesta.
7. Devuelve un nuevo estado para continuar el grafo.

---

## Ejemplo de uso del sistema

### Paso 1: Guardar número de cliente

```
POST /a6memory/query
{
  "user_id": "fran.aragon",
  "question": "Mi número de cliente era 9843, recuérdalo."
}
```

→ La respuesta del modelo se guarda automáticamente como memoria.

### Paso 2: Preguntar por número de cliente

```
POST /a6memory/query
{
  "user_id": "fran.aragon",
  "question": "¿Cuál era mi número de cliente?"
}
```

Resultado:

```json
{
  "answer": "Tu número de cliente guardado es 9843.",
  "memory_used": ["buffer"]
}
```

### Paso 3: Preguntar por banco

```
POST /a6memory/query
{
  "user_id": "fran.aragon",
  "question": "¿Cuál es mi banco?"
}
```

Resultado:

```json
{
  "answer": "Tu banco es BBVA.",
  "memory_used": ["buffer"]
}
```

> Nota: Gracias al prompt optimizado, el LLM **solo responde a la pregunta actual**, aunque existan otros datos guardados en memoria.

---

## Notas finales

* Sistema simple, extensible y didáctico.
* Permite añadir embeddings, resúmenes avanzados, filtros de memoria, top-k dinámico, etc.
* Almacenamiento persistente y multiusuario gracias a ChromaDB.
* Respuestas concretas y precisas gracias al prompt optimizado que ignora datos irrelevantes.


