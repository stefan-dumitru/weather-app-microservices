from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_in)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_in)