from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.services.location_service import (
    create_location,
    get_user_locations,
    delete_location,
    update_location
)

router = APIRouter(prefix="/location", tags=["Location"])

@router.post("/", response_model=LocationResponse)
def add_location(
    location: LocationCreate,
    user_id: int,                     # user_id comes from API Gateway
    db: Session = Depends(get_db)
):
    return create_location(db, user_id, location)

@router.get("/", response_model=list[LocationResponse])
def list_locations(
    user_id: int,                     # user_id comes from API Gateway
    db: Session = Depends(get_db)
):
    return get_user_locations(db, user_id)

@router.delete("/{loc_id}")
def remove_location(loc_id: int, db: Session = Depends(get_db), user_id: int = 1):
    return delete_location(db, user_id, loc_id)

@router.put("/{loc_id}", response_model=LocationResponse)
def edit_location(loc_id: int, update: LocationUpdate, db: Session = Depends(get_db), user_id: int = 1):
    return update_location(db, user_id, loc_id, update)