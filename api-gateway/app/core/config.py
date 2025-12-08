from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str
    LOCATION_SERVICE_URL: str
    WEATHER_SERVICE_URL: str
    ALERT_SERVICE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    VAPID_PUBLIC_KEY: str
    VAPID_PRIVATE_KEY: str
    VAPID_EMAIL: str

    ALLOWED_ORIGIN_1 : str
    ALLOWED_ORIGIN_2 : str

    class Config:
        env_file = ".env"

settings = Settings()