from fastapi import FastAPI
from app.api.v1.routes_weather import router as weather_router

app = FastAPI(title="Weather Service")

app.include_router(weather_router)