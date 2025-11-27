from langchain_core.prompts import PromptTemplate

classifier_prompt = PromptTemplate.from_template("""
Clasifica la siguiente pregunta en una de las siguientes categorías:

- general → preguntas abiertas, explicaciones, creatividad, conversación normal.
- rag → preguntas que requieren usar información REAL proveniente de documentos, base de conocimiento o datos externos. Palabras clave: "documento", "según el texto", "qué dice", "extrae del archivo", "basado en el material", "qué indican los datos".
- summary → cuando se pide RESUMIR un texto proporcionado por el usuario. Solo se clasifica como summary si el usuario claramente proporciona texto para ser resumido.
- code → preguntas relacionadas con programación, errores, generación de funciones, fragmentos de código, debugging.
- math → problemas matemáticos, cálculos, expresiones numéricas, ecuaciones o razonamiento matemático.

Reglas importantes:
1. Si la pregunta pide resumir contenido proporcionado por el usuario → summary.
2. Si la pregunta pide extraer, buscar o consultar información de un documento, PDF, manual o contexto → rag.
3. Si no está claro que es summary o rag → clasificar como general.
4. Responde SOLO con una palabra EXACTA de esta lista:
general, rag, summary, code, math

Pregunta: "{input}"

Tu respuesta:
""")


general_prompt = PromptTemplate.from_template("""
Responde de forma clara y precisa:
{input}
""")

code_prompt = PromptTemplate.from_template("""
Eres un asistente experto en Python. Ayuda al usuario con su código:
{input}
""")

summary_prompt = PromptTemplate.from_template("""
Resume el siguiente contenido de manera clara:
{input}
""")

math_prompt = PromptTemplate.from_template("""
Resuelve el siguiente ejercicio paso a paso, pero devuelve solo el resultado final:
{input}
""")

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

Contexto recuperado:
{context}

Pregunta:
{input}

Respuesta:
""")

