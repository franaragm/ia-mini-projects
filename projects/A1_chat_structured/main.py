from fastapi import APIRouter
from .router import router as a1_router

router = APIRouter()
router.include_router(a1_router)
