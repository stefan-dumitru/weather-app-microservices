from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str