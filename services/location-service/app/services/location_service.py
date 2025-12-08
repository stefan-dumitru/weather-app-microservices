from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.location import LocationCreate
from app.db.models import Location

def create_location(db: Session, user_id: int, location: LocationCreate):
    db_location = models.Location(
        user_id=user_id,
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_user_locations(db: Session, user_id: int):
    return db.query(models.Location).filter(models.Location.user_id == user_id).all()

def delete_location(db, user_id, loc_id):
    loc = db.query(Location).filter(Location.id == loc_id, Location.user_id == user_id).first()
    if not loc:
        raise HTTPException(404, "Location not found")
    db.delete(loc)
    db.commit()
    return {"message": "Location deleted"}

def update_location(db, user_id, loc_id, update):
    loc = db.query(Location).filter(Location.id == loc_id, Location.user_id == user_id).first()
    if not loc:
        raise HTTPException(404, "Location not found")

    if update.name is not None:
        loc.name = update.name
    if update.latitude is not None:
        loc.latitude = update.latitude
    if update.longitude is not None:
        loc.longitude = update.longitude

    db.commit()
    db.refresh(loc)
    return loc