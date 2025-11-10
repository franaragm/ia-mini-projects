from pydantic import BaseModel, Field

class IntentRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario")

class IntentResponse(BaseModel):
    action: str = Field(..., description="Tipo de acción que el usuario quiere realizar")
    title: str | None = Field(None, description="Título si aplica (por ejemplo crear tarea)")
    due_date: str | None = Field(None, description="Fecha en formato YYYY-MM-DD si aplica")
