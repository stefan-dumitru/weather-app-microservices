from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.schemas.user import UserCreate, UserLogin
from app.utils.hashing import hash_password, verify_password
from app.utils.security import create_access_token

def register_user(db: Session, user_in: UserCreate):
    # check if email exists already
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login_user(db: Session, user_in: UserLogin):
    user = db.query(models.User).filter(models.User.email == user_in.email).first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}