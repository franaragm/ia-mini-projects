from openai import OpenAI
from .utils import get_env

OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = get_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_DEFAULT_MODEL = get_env("DEFAULT_MODEL", "meta-llama/llama-3.3-8b-instruct:free")

# Cliente compatible con OpenAI, apuntado a OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

async def ask_model(prompt: str):
    response = client.chat.completions.create(
        model=OPENROUTER_DEFAULT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
        top_p=0.9,
    )
    return response.choices[0].message.content
