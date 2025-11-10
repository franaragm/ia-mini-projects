from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_client import llm
from .prompts import chat_template
import json

router = APIRouter(prefix="/a1", tags=["A1 - Chat estructurado"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def structured_chat(req: ChatRequest):
    prompt = chat_template.format(user_message=req.message)
    response = await llm(prompt)
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        data = {"response": response.strip(), "razonamiento": "El modelo no devolvió JSON puro."}

    return data
