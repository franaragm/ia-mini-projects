from openai import AsyncOpenAI
from .utils import get_env
from config_base import DEFAULT_LLM_MODEL

OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = get_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Cliente compatible con OpenAI, apuntado a OpenRouter
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

async def llm(prompt: str):
    response = await client.chat.completions.create(
        model=DEFAULT_LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
        top_p=0.9,
    )
    return response.choices[0].message.content
