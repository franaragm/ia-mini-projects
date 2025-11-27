from pydantic import BaseModel, Field

class A5Request(BaseModel):
    question: str = Field(..., example="¿Qué es un embedding?")

class A5Response(BaseModel):
    intent: str
    chain_used: str
    answer: str
