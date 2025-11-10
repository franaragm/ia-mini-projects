from langchain_core.prompts import PromptTemplate

intent_prompt = PromptTemplate.from_template("""
Eres un asistente que analiza mensajes de usuario y devuelve un JSON con intención estructurada.

Formato obligatorio (usa exactamente este formato, sin texto fuera del JSON):

{{
  "action": "create_task | update_task | get_status | other",
  "title": "texto o null",
  "due_date": "YYYY-MM-DD o null"
}}

No expliques tu razonamiento.
No añadas texto extra.
No digas "Aquí tienes el JSON".

Usuario: {user_message}

Respuesta JSON:
""")

