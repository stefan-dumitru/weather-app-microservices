import httpx
from app.core.config import settings

async def create_location(data: dict, user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.LOCATION_SERVICE_URL}/location/",
            params={"user_id": user_id},
            json=data
        )
        return response.json(), response.status_code

async def read_locations(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.LOCATION_SERVICE_URL}/location/",
            params={"user_id": user_id}
        )
        return response.json(), response.status_code

async def delete_location(loc_id: int, user_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"{settings.LOCATION_SERVICE_URL}/location/{loc_id}",
            params={"user_id": user_id},
        )
        return r.json(), r.status_code

async def edit_location(loc_id: int, data: dict, user_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{settings.LOCATION_SERVICE_URL}/location/{loc_id}",
            params={"user_id": user_id},
            json=data
        )
        return r.json(), r.status_code