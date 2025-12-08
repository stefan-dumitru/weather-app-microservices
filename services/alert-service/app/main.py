import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.routes_alerts import router as alerts_router
from app.services.alert_service import alert_monitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting background alert monitor...")
    task = asyncio.create_task(alert_monitor())  # RUNS BACKGROUND TASK

    yield  # App is running here

    print("🛑 Stopping alert monitor...")
    task.cancel()


app = FastAPI(title="Alert Service", lifespan=lifespan)

app.include_router(alerts_router)