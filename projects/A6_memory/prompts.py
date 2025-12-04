from langchain_core.prompts import PromptTemplate

memory_preparation_prompt = PromptTemplate.from_template("""
Eres un asistente que transforma la información relevante del usuario en memoria estructurada.
Usuario dice:
{input}

Extrae la información que deba ser recordada y devuelve solo el texto a guardar en memoria.
Si no hay información para recordar, devuelve un string vacío.
""")

memory_prompt = PromptTemplate.from_template("""
Eres un asistente que recuerda información del usuario.
Memoria relevante del usuario:
{memory}

Pregunta del usuario:
{input}

Instrucciones:
- Responde únicamente a la pregunta que se hace.
- No incluyas información de la memoria que no sea estrictamente necesaria.
- Sé concreto, claro y breve.
- No te limites a pegar la memoria; intégrala en la respuesta.
- Si la respuesta requiere un dato específico de la memoria, inclúyelo; de lo contrario, ignora los demás datos.

Respuesta:
""")
