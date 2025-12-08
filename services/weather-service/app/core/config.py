from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WEATHER_API_KEY: str
    WEATHER_API_URL: str
    DEFAULT_UNITS: str

    class Config:
        env_file = ".env"

settings = Settings()