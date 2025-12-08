from fastapi import APIRouter
from app.services.weather_service import fetch_current_weather, fetch_week_forecast
from app.schemas.weather import WeatherCurrent, WeatherWeek

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current", response_model=WeatherCurrent)
async def get_current_weather(lat: float, lon: float):
    return await fetch_current_weather(lat, lon)

@router.get("/week", response_model=WeatherWeek)
async def get_week_forecast(lat: float, lon: float):
    return await fetch_week_forecast(lat, lon)