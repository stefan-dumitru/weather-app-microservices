from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    WEATHER_SERVICE_URL: str
    API_GATEWAY_URL: str

    class Config:
        env_file = ".env"

settings = Settings()