from fastapi import APIRouter

from app.api.endpoints import parts

api_router = APIRouter()
api_router.include_router(parts.router, prefix="/parts", tags=["parts"])