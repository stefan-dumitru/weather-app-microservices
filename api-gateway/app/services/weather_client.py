import httpx
from app.core.config import settings

async def get_current_weather(lat: float, lon: float):
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{settings.WEATHER_SERVICE_URL}/weather/current",
            params={"lat": lat, "lon": lon}
        )

        return response.json(), response.status_code

async def get_week_forecast(lat: float, lon: float):
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{settings.WEATHER_SERVICE_URL}/weather/week",
            params={"lat": lat, "lon": lon}
        )

        return response.json(), response.status_code