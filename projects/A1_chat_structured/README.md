# A1 - Chat Estructurado (Prompt Template + Respuesta Tipada)

Objetivo: aprender a controlar la respuesta del modelo usando prompts estructurados.

Este endpoint recibe un `prompt` y devuelve una respuesta que **siempre cumple** la estructura JSON:

```json
{
  "answer": "texto",
  "tone": "educational | casual | formal",
  "metadata": {
    "model": "string",
    "tokens_used": number
  }
}
