from fastapi import APIRouter

from app.api.routes import items, login, users, utils, signup, contactus

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(signup.router, prefix="/signup", tags=["signup"])
api_router.include_router(contactus.router, prefix="/contactus", tags=["contactus"])
