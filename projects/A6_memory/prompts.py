from langchain_core.prompts import PromptTemplate

memory_preparation_prompt = PromptTemplate.from_template("""
Eres un asistente encargado de convertir en memoria la información relevante que el usuario quiera que recuerdes.

Usuario dice:
{input}

Instrucciones:
- Extrae únicamente información que sea útil recordar (como datos personales, preferencias, números, bancos, etc.).
- No te limites a guardar solo un numero o dato, guardalo junto con su contexto para que tenga sentido.
- No guardes afirmaciones sin contenido útil.
- No generes espacios en blanco, saltos de línea ni caracteres invisibles.
- Si no hay nada que recordar, devuelve un guion medio (-) para indicar que no se debe guardar nada.

Texto para memoria:
""")

memory_prompt = PromptTemplate.from_template("""
Eres un asistente que recuerda información del usuario.

Memoria relevante del usuario:
{memory}

Pregunta del usuario:
{input}

Instrucciones estrictas:
1. Si el mensaje del usuario es una AFIRMACIÓN (no contiene pregunta y comunica un dato), responde únicamente:
   ok
2. Si es una PREGUNTA aunque no tenga signos de interrogación, responde solo a esa pregunta.
3. Usa la memoria solo si es estrictamente necesaria para responder.
4. No añadas información adicional que el usuario no haya pedido.
5. No repitas datos que el usuario acaba de decir.
6. Mantén la respuesta breve, directa y sin adornos. Pero sin limitar la información necesaria. Y sin olvidar ningún dato importante.
7. Si no tienes suficiente información en la memoria para responder, di "No lo sé".
8. No inventes datos ni respuestas.
9. No te limites a repetir la memoria, intégrala en la respuesta.


Respuesta:
""")