from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Eres un asistente experto en IA. Usa el siguiente contexto comprimido para responder con precisión a la pregunta planteada.

No inventes información. Si no sabes algo, di "No tengo información suficiente en los documentos".

=== CONTEXTO ===
{context}

=== PREGUNTA ===
{question}

""")
