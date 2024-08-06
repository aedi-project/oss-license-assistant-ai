from fastapi import APIRouter

from app.api.routes import items, oauth, users

api_router = APIRouter()
api_router.include_router(oauth.router, tags=["oauth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
