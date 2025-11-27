from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Eres un asistente especializado en RAG. Debes responder **únicamente** con la información que aparezca en el siguiente contexto. 
No inventes datos, no agregues conocimiento externo y no uses información general que no esté contenida explícitamente en el contexto.

Si el contexto no contiene información suficiente para responder la pregunta, responde exactamente:
"Sin suficiente información en la documentación para responder."

Produce una respuesta:
- Clara, concisa y directa.
- Basada solo en detalles presentes en el contexto.
- Sintetizando y explicando, no copiando el contexto textual sin procesarlo.
- Sin añadir interpretaciones no justificadas por el contenido.

Documentos relevantes de contexto:
{context}

Pregunta del usuario:
{question}
""")
