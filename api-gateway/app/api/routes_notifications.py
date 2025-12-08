from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

router = APIRouter(prefix="/notifications", tags=["Notifications"])

async def event_generator():
    counter = 0
    while True:
        # This is a test event
        alert = {
            "id": counter,
            "message": f"Test alert #{counter}"
        }

        yield f"data: {json.dumps(alert)}\n\n"

        counter += 1
        await asyncio.sleep(5)  # send alert every 5 seconds


@router.get("/stream")
async def stream_notifications():
    return StreamingResponse(event_generator(), media_type="text/event-stream")