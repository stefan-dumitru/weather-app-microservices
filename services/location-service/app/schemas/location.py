from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class LocationResponse(LocationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True