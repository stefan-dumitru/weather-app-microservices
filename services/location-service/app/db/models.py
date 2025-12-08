from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String)
    # latitude = Column(String)
    # longitude = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)