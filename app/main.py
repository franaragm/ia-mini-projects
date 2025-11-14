from fastapi import FastAPI
from .routes import router
from .services.utils import get_env

ENV = get_env("ENV", "dev")  # dev | prod

docs_url = "/docs" if ENV == "dev" else None
redoc_url = "/redoc" if ENV == "dev" else None
openapi_url = "/openapi.json" if ENV == "dev" else None

app = FastAPI(
    title="LangChain Lab - AI Server",
    description="""
    Servidor de experimentación con modelos de IA, RAG y agentes.

    Este backend expone APIs para explorar:
    - Recuperación aumentada con generación (RAG)
    - Llamadas a modelos LLM
    - Herramientas generativas
    - Proyectos modulares de IA

    """,
    version="1.0.0",
    summary="Backend laboratorio para proyectos de IA",
    contact={
        "name": "Francisco Aragón",
        "email": "franaragonmesa@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

app.include_router(router)
