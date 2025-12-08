from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as user_router
from app.api.routes_location import router as location_router
from app.api.routes_weather import router as weather_router
from app.api.routes_alerts import router as alerts_router
from app.api.routes_notifications import router as notifications_router
from app.core.config import settings

app = FastAPI(title="API Gateway")

origins = [ settings.ALLOWED_ORIGIN_1, settings.ALLOWED_ORIGIN_2 ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(user_router)
app.include_router(location_router)
app.include_router(weather_router)
app.include_router(alerts_router)
app.include_router(notifications_router)