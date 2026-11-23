from fastapi import APIRouter, FastAPI



from .routes import users, products, shops, address, orders, payments


api_router = APIRouter()
api_router.include_router(users.router)