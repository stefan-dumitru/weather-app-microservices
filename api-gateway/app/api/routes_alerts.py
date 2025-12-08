from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from app.core.security import validate_token
from app.services.alert_client import create_alert, get_alerts
import asyncio

from pywebpush import webpush, WebPushException
from app.core.config import settings


router = APIRouter(prefix="/alerts", tags=["Alerts"])

# ---- STORAGE ----
subscribers = set()      # SSE (browser open)
push_subscriptions = []  # Push notification devices


# ---- CRUD ----
@router.post("/")
async def gateway_create_alert(data: dict, payload=Depends(validate_token)):
    user_id = payload["sub"]
    result, status = await create_alert(data, user_id)
    return result


@router.get("/")
async def gateway_get_alerts(payload=Depends(validate_token)):
    user_id = payload["sub"]
    result, status = await get_alerts(user_id)
    return result


# ---- SSE STREAM ----
async def event_stream():
    queue = asyncio.Queue()
    subscribers.add(queue)

    try:
        while True:
            message = await queue.get()
            yield f"data: {message}\n\n"
    finally:
        subscribers.remove(queue)


def broadcast_sse(message: str):
    """Send to open UI tabs"""
    for queue in subscribers:
        queue.put_nowait(message)


def send_push(message: str):
    """Send system notifications to ALL devices"""
    for sub in push_subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=message,
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": settings.VAPID_EMAIL},
            )
        except WebPushException as e:
            print("❌ Push delivery failed:", e)


@router.get("/stream")
async def alerts_stream(request: Request):
    token = request.query_params.get("token")
    if not token:
        raise HTTPException(401, "Missing token")

    validate_token(token)
    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ---- NOTIFY FROM ALERT SERVICE ----
@router.post("/notify")
async def notify_alert(data: dict):
    message = data.get("message", "Unknown alert")
    
    # UI and Push
    broadcast_sse(message)
    send_push(message)

    return {"status": "ok", "broadcasted": message}


# ---- SUBSCRIBE FOR PUSH ----
@router.post("/subscribe")
async def subscribe_push(subscription: dict):
    print("📩 New Push Subscription received")

    if subscription not in push_subscriptions:
        push_subscriptions.append(subscription)

    return {"status": "subscribed"}