from fastapi import APIRouter

from .auth import router as auth_router
from .default import router as default_router


api_v1_router = APIRouter(prefix="/api/v1")
# Добавляем роутеры


main_router = APIRouter()
main_router.include_router(auth_router, tags=["Auth"])
main_router.include_router(default_router, tags=["HomePage"])
main_router.include_router(api_v1_router)
