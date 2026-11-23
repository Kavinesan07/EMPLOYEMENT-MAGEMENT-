from fastapi import APIRouter, FastAPI
from routes import user


api_router = APIRouter()
api_router.include_router(user.router)