from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alert import AlertCreate, AlertResponse
from app.services.alert_service import create_alert, get_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/", response_model=AlertResponse)
def add_alert(alert: AlertCreate, user_id: int, db: Session = Depends(get_db)):
    return create_alert(db, user_id, alert)

@router.get("/", response_model=list[AlertResponse])
def list_alerts(user_id: int, db: Session = Depends(get_db)):
    return get_alerts(db, user_id)