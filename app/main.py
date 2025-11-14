from fastapi import FastAPI
from .routes import router

app = FastAPI(title="LangChain Lab - AI Server")

app.include_router(router)
