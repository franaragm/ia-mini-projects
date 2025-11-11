from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Utiliza únicamente la información proporcionada para responder al usuario.
Si no encuentras la respuesta en los documentos, responde:
"No encuentro esa información en los documentos."

Documentos relevantes:
{context}

Pregunta del usuario:
{question}
""")
