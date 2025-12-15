from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alert import AlertCreate, AlertResponse
from app.services.alert_service import create_alert, get_alerts
from app.models.alert import Alert
from fastapi import HTTPException

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/", response_model=AlertResponse)
def add_alert(alert: AlertCreate, user_id: int, db: Session = Depends(get_db)):
    return create_alert(db, user_id, alert)

@router.get("/", response_model=list[AlertResponse])
def list_alerts(user_id: int, db: Session = Depends(get_db)):
    return get_alerts(db, user_id)

@router.patch("/{alert_id}/toggle", response_model=AlertResponse)
def toggle_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(404, "Alert not found")

    alert.active = not alert.active
    db.commit()
    db.refresh(alert)
    return alert


@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(404, "Alert not found")

    db.delete(alert)
    db.commit()
    return {"status": "deleted"}