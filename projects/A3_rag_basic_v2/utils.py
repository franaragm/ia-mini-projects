import json
from .schemas import QueryResponse

def safe_json_parse(text: str):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {"answer": text.strip(), "sources": []}

    # Validamos estructura con Pydantic
    try:
        parsed = QueryResponse(**data)
    except Exception as e:
        return {
            "error": "La estructura JSON no cumple el esquema esperado",
            "details": str(e),
            "raw_data": data,
            "answer": text.strip(),
            "sources": []
        }

    return parsed