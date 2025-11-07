from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Mini Projects LangChain - Base Server")

app.include_router(router)
