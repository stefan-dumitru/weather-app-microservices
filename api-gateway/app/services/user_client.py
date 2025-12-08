import httpx
from app.core.config import settings

async def user_login(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.USER_SERVICE_URL}/auth/login", json=data)
        return response.json(), response.status_code

async def user_register(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.USER_SERVICE_URL}/auth/register", json=data)
        return response.json(), response.status_code