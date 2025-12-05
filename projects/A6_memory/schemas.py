from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Representa un mensaje dentro del historial del chat.
# Se usa en el grafo y en la persistencia del estado.
class Message(BaseModel):
    role: str            # "user" o "assistant"
    content: str         # Texto del mensaje


# Estado completo utilizado por el grafo de LangGraph.
# Contiene la información necesaria para ejecutar cada nodo
# y pasar datos entre ellos.
class ChatState(BaseModel):
    user_id: Optional[str] = None            # Identificador del usuario (para memoria en ChromaDB)
    messages: Optional[List[Message]] = None # Conversación hasta el momento
    summary: Optional[str] = None            # Resumen de los últimos mensajes (generado por el grafo)
    meta: Optional[Dict[str, Any]] = None    # Información adicional para seguimiento del flujo (última pregunta, etc.)


# Esquema del body recibido por el endpoint POST /query.
# Representa la pregunta del usuario junto con su user_id.
class MemoryQuery(BaseModel):
    user_id: str = Field(..., example="fran.aragon")  
    question: str = Field(..., example="Mi número de cliente era 9843, recuérdalo.")


# Respuesta del endpoint /query.
# Contiene la respuesta generada por el asistente
# y qué tipo de memoria fue utilizada (summary, buffer, etc.).
class MemoryResponse(BaseModel):
    answer: str              # Respuesta final del asistente
    memory_used: List[str]   # Lista de memorias consultadas o generadas durante el proceso
    
# Nuevo esquema para el endpoint GET /memory_state/{user_id}
class MemoryStateResponse(BaseModel):
    user_id: str               # Identificador del usuario
    memory: List[str]          # Lista de textos de memoria asociados al usuario

# Respuesta estándar para endpoints que solo deben indicar éxito,
# como el borrado de memoria.
class EmptyResponse(BaseModel):
    ok: bool                 # True si la operación fue exitosa
