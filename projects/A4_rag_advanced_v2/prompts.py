from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Eres un asistente experto en IA. Usa el siguiente contexto recuperado de los documentos
para responder a la pregunta del usuario de manera precisa, concisa y verificada.

No inventes información. Si no sabes algo, di "No tengo información suficiente en los documentos".

=== CONTEXTO ===
{context}

=== PREGUNTA ===
{question}

""")
