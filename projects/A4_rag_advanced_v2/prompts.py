from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Eres un asistente experto en IA. Usa el siguiente contexto comprimido para responder con precisión a la pregunta planteada.

Usa **solo** la información del contexto si es relevante.
No inventes información. Si no hay suficiente información en el contexto, indica que no puedes responder con precisión.
Si no hay suficiente información en el contexto, di "No tengo información suficiente en los documentos".
Responde de manera concisa, precisa, verificada y sin limitarse a pegar fragmentos del contexto.

=== CONTEXTO ===
{context}

=== PREGUNTA ===
{question}

""")
