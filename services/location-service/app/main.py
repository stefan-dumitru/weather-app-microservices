from fastapi import FastAPI
from app.api.v1.routes_location import router

app = FastAPI(title="Location Service")

app.include_router(router)