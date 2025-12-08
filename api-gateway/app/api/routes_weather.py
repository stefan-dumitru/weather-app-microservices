from fastapi import APIRouter, Depends
from app.core.security import validate_token
from app.services.weather_client import get_current_weather, get_week_forecast

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current")
async def gateway_current_weather(lat: float, lon: float, payload=Depends(validate_token)):
    data, status = await get_current_weather(lat, lon)
    return data

@router.get("/week")
async def gateway_week_weather(lat: float, lon: float, payload=Depends(validate_token)):
    data, status = await get_week_forecast(lat, lon)
    return data