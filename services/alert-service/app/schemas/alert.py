from pydantic import BaseModel

class AlertBase(BaseModel):
    city_name: str
    latitude: float
    longitude: float
    condition: str
    threshold: float
    day_range: int = 0

class AlertCreate(AlertBase):
    active: bool = True

class AlertResponse(AlertBase):
    id: int
    user_id: int
    active: bool

    class Config:
        from_attributes = True