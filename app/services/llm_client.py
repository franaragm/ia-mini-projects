from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from .utils import get_env
from config_base import DEFAULT_LLM_MODEL, FALLBACK_LLM_MODEL

OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = get_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Cliente OpenRouter compatible con AsyncOpenAI
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

# ============================================================
# 1) Cliente simple (para proyectos casuales o endpoints básicos)
# ============================================================

# Cliente minimalista para prompts directos sin LangChain. Devuelve solo texto. Ideal para endpoints simples.
async def llm(prompt: str, model: str | None = None) -> str:
    model_to_use = model or DEFAULT_LLM_MODEL
    params = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    try:
        response = await client.chat.completions.create(model=model_to_use, **params)

    except Exception:
        # Reintento limpio usando fallback
        response = await client.chat.completions.create(model=FALLBACK_LLM_MODEL, **params)

    return response.choices[0].message.content

# ============================================================
# 2) Cliente especial para Chains LangChain
# ============================================================

# Devuelve un objeto ChatOpenAI configurado para OpenRouter. Compatible con LLMChain, RouterChain, MultiPromptChain, agentes, etc.
def llm_chain(model: str | None = None, temperature: float = 0.0,) -> ChatOpenAI:
    model_to_use = model or DEFAULT_LLM_MODEL

    llm_params = {
        "api_key": OPENROUTER_API_KEY,
        "base_url": OPENROUTER_BASE_URL,
        "temperature": temperature,
    }

    try:
        return ChatOpenAI(model=model_to_use, **llm_params)
    except Exception:
        return ChatOpenAI(model=FALLBACK_LLM_MODEL, **llm_params)