from sqlalchemy import Column, Integer, String, Float, Boolean, Numeric
from app.db.session import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # from JWT
    city_name = Column(String, index=True)
    # latitude = Column(Float)
    # longitude = Column(Float)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    condition = Column(String)  # ex: "rain", "snow", "temp_below"
    threshold = Column(Float)   # ex: temperature < 5
    active = Column(Boolean, default=True)