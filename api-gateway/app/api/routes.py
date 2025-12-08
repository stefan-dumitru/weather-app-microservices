from fastapi import APIRouter, Depends
from app.services.user_client import user_login, user_register
from app.core.security import validate_token

router = APIRouter()

@router.post("/auth/login")
async def gateway_login(data: dict):
    result, status = await user_login(data)
    return result

@router.post("/auth/register")
async def gateway_register(data: dict):
    return await user_register(data)

@router.get("/protected")
async def protected_route(payload: dict = Depends(validate_token)):
    return {"message": "You are authenticated!", "user": payload}