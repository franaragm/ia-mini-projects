from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., example="Qué es la inteligencia artificial?")

class QueryResponse(BaseModel):
    response: str = Field(..., description="Respuesta generada por el modelo LLM")
    sources: list[str] = Field(..., description="Documentos utilizados para generar la respuesta")