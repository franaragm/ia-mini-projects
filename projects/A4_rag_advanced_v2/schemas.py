from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., example="Qué son las Redes Neuronales Convolucionales?")

class SourceDocument(BaseModel):
    source: str = Field(..., description="Ruta o nombre del documento de origen")
    score: float = Field(..., description="Similitud o relevancia del documento recuperado")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Respuesta generada por el modelo")
    sources: list[SourceDocument] = Field(..., description="Documentos usados para generar la respuesta")
