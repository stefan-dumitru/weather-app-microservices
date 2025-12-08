import asyncio
import httpx
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.schemas.alert import AlertCreate
from app.core.config import settings
from app.db.session import SessionLocal

# CREATE ALERT

def create_alert(db: Session, user_id: int, alert: AlertCreate):
    db_alert = Alert(
        user_id=user_id,
        city_name=alert.city_name,
        latitude=alert.latitude,
        longitude=alert.longitude,
        condition=alert.condition,
        threshold=alert.threshold,
        active=True
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

# GET ALERTS

def get_alerts(db: Session, user_id: int):
    return db.query(Alert).filter(Alert.user_id == user_id).all()

# GET WEATHER FROM WEATHER SERVICE

async def get_weather(lat: float, lon: float):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.WEATHER_SERVICE_URL}/weather/current",
            params={"lat": lat, "lon": lon}
        )
        return response.json()

# CHECK IF ALERT IS TRIGGERED

def check_condition(alert, weather):
    condition = alert.condition
    threshold = alert.threshold

    temp = weather.get("temperature")
    desc = weather.get("description", "").lower()
    wind = weather.get("wind_speed")

    if condition == "rain":
        return "rain" in desc

    if condition == "snow":
        return "snow" in desc

    if condition == "temp_below":
        return temp is not None and temp < threshold

    if condition == "temp_above":
        return temp is not None and temp > threshold

    if condition == "wind_above":
        return wind is not None and wind > threshold

    if condition == "wind_below":
        return wind is not None and wind < threshold

    return False

# SEND NOTIFICATIONS TO API GATEWAY (SSE BROADCAST)

API_GATEWAY_URL = settings.API_GATEWAY_URL

async def alert_monitor():
    while True:
        print("🔎 Checking alerts...")

        db: Session = SessionLocal()
        alerts = db.query(Alert).filter(Alert.active == True).all()

        for alert in alerts:
            try:
                weather = await get_weather(alert.latitude, alert.longitude)
            except Exception as e:
                print("❌ Weather fetch failed:", repr(e))
                continue

            if check_condition(alert, weather):
                message = f"🚨 ALERT TRIGGERED in {alert.city_name}! Condition: {alert.condition}"
                print(message)

                # Notify API Gateway
                async with httpx.AsyncClient() as client:
                    try:
                        await client.post(
                            f"{API_GATEWAY_URL}/alerts/notify",
                            json={"message": message}
                        )
                    except Exception as e:
                        print("❌ Failed to notify gateway:", e)

                # Disable alert
                # alert.active = False
                db.commit()

        db.close()

        await asyncio.sleep(10)