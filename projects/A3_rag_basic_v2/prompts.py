from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Eres un asistente que responde usando la información de contexto proporcionada.

Usa **solo** la información del contexto si es relevante.
Si no hay suficiente información, indica que no puedes responder con precisión.

### Contexto:
{context}

### Pregunta:
{question}

Devuelve un JSON con este formato:

{{
  "answer": "<respuesta del asistente>",
  "sources": ["fragmento 1", "fragmento 2", ...]
}}
""")