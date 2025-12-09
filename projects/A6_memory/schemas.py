from pydantic import BaseModel, Field
from typing import List

class MemoryQuery(BaseModel):
    user_id: str = Field(..., example="fran.aragon")
    question: str = Field(..., example="Mi número de cliente era 9843, recuérdalo.")

class MemoryResponse(BaseModel):
    answer: str
    memory_used: List[dict]

class MemoryStateResponse(BaseModel):
    user_id: str
    memory: List[str]

class EmptyResponse(BaseModel):
    ok: bool
