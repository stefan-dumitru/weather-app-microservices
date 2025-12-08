import httpx
from app.core.config import settings

async def fetch_current_weather(lat: float, lon: float):
    url = f"{settings.WEATHER_API_URL}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.WEATHER_API_KEY,
        "units": settings.DEFAULT_UNITS
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url, params=params)
            r.raise_for_status()  # ensures we detect 400/500 errors
        except httpx.HTTPError as e:
            print(f"❌ Weather API call failed: {e}")
            return {
                "temperature": None,
                "description": "Unavailable",
                "humidity": None,
                "wind_speed": None
            }

    data = r.json()

    return {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

async def fetch_week_forecast(lat: float, lon: float):
    url = f"{settings.WEATHER_API_URL}/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.WEATHER_API_KEY,
        "units": settings.DEFAULT_UNITS
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url, params=params)
            r.raise_for_status()
        except httpx.HTTPError as e:
            print(f"❌ Weather API (forecast) failed: {e}")
            return {"days": []}

    data = r.json()

    days = []
    used_dates = set()

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]

        if date in used_dates:
            continue
        
        used_dates.add(date)

        days.append({
            "date": date,
            "temperature_min": entry["main"]["temp_min"],
            "temperature_max": entry["main"]["temp_max"],
            "description": entry["weather"][0]["description"],
        })

        if len(days) == 7:
            break

    return {"days": days}