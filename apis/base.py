from fastapi import APIRouter

from apis.v1 import router_user
from apis.v1 import router_message
from apis.v1 import router_chat


api_router = APIRouter()
api_router.include_router(router_user.router, prefix="/user", tags=["User"])
api_router.include_router(router_message.router, prefix="/message", tags=["Message"])
api_router.include_router(router_chat.router, prefix="/chat", tags=["Chat"])
