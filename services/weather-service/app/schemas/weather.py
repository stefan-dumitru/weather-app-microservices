from pydantic import BaseModel

class WeatherCurrent(BaseModel):
    temperature: float
    description: str
    humidity: int
    wind_speed: float

class WeatherDaily(BaseModel):
    date: str
    temperature_min: float
    temperature_max: float
    description: str

class WeatherWeek(BaseModel):
    days: list[WeatherDaily]