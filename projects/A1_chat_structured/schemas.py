from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., example="Define que es un chatbot estructurado")

class ResponseMetadata(BaseModel):
    model: str = Field(..., description="Nombre del modelo usado para generar la respuesta")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Texto final que entregamos al usuario")
    tone: str = Field(..., description="Tono de la respuesta (por ejemplo: educational, friendly, formal, etc.)")
    metadata: ResponseMetadata = Field(..., description="Información adicional sobre la generación")