from fastapi import APIRouter, FastAPI
from app.routes import admin
from routes import user



api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(admin.router)
