from fastapi import FastAPI
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_users import router as users_router

app = FastAPI(title="User Service")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])