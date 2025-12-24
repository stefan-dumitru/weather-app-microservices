import asyncio
import httpx
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.schemas.alert import AlertCreate
from app.core.config import settings
from app.db.session import SessionLocal
from datetime import datetime, date, timezone, timedelta

# CREATE ALERT

def create_alert(db: Session, user_id: int, alert: AlertCreate):
    db_alert = Alert(
        user_id=user_id,
        city_name=alert.city_name,
        latitude=alert.latitude,
        longitude=alert.longitude,
        condition=alert.condition,
        threshold=alert.threshold,
        day_range=alert.day_range,
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
    
# GET WEEK WEATHER FROM WEATHER SERVICE

async def get_week_weather(lat: float, lon: float):
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{settings.WEATHER_SERVICE_URL}/weather/week",
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

def check_condition_for_day(alert, day_weather):
    temp_min = day_weather.get("temperature_min")
    temp_max = day_weather.get("temperature_max")
    desc = day_weather.get("description", "").lower()
    wind = day_weather.get("wind_speed")

    if alert.condition == "rain":
        return "rain" in desc

    if alert.condition == "snow":
        return "snow" in desc

    if alert.condition == "temp_below":
        return temp_min is not None and temp_min < alert.threshold

    if alert.condition == "temp_above":
        return temp_max is not None and temp_max > alert.threshold
    
    if alert.condition == "wind_above":
        return wind is not None and wind > alert.threshold

    if alert.condition == "wind_below":
        return wind is not None and wind < alert.threshold

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
                forecast = await get_week_weather(alert.latitude, alert.longitude)
            except Exception as e:
                print("❌ Weather fetch failed:", repr(e))
                continue

            days = forecast.get("days", [])

            # Limit days based on alert range (today + day_range)
            max_days = min(alert.day_range + 1, len(days))

            for i in range(max_days):
                day = days[i]
                day_date = date.fromisoformat(day["date"])

                # ❗ Avoid duplicate notifications for same day
                if alert.last_triggered_at:
                    if alert.last_triggered_at.date() == day_date:
                        continue

                if check_condition_for_day(alert, day):
                    message = f"🚨 ALERT in {alert.city_name} 📅 Date: {day_date} ⚠ Condition: {alert.condition}"

                    print(message)

                    async with httpx.AsyncClient() as client:
                        try:
                            await client.post(
                                f"{API_GATEWAY_URL}/alerts/notify",
                                json={"message": message}
                            )
                        except Exception as e:
                            print("❌ Failed to notify gateway:", e)

                    # Mark alert as triggered for this day
                    alert.last_triggered_at = datetime.now(timezone.utc) + timedelta(hours=2)
                    db.commit()

                    # Small pause to avoid burst notifications
                    await asyncio.sleep(10)

        db.close()
        await asyncio.sleep(60)