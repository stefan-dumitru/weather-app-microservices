import httpx
from app.core.config import settings

async def create_alert(data: dict, user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.ALERT_SERVICE_URL}/alerts/",
            params={"user_id": user_id},
            json=data
        )
        return response.json(), response.status_code

async def get_alerts(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.ALERT_SERVICE_URL}/alerts/",
            params={"user_id": user_id}
        )
        return response.json(), response.status_code