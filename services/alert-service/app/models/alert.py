from sqlalchemy import Column, Integer, String, Float, Boolean, Numeric, DateTime
from app.db.session import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # from JWT
    city_name = Column(String, index=True)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    condition = Column(String)  # ex: "rain", "snow", "temp_below"
    threshold = Column(Float)   # ex: temperature < 5
    active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime, nullable=True)
    day_range = Column(Integer, default=0, nullable=False)  # 0 means every day, 1 means today and tomorrow, etc.