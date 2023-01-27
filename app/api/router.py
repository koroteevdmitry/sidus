from fastapi.routing import APIRouter

from api.user.controller import router as users_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
