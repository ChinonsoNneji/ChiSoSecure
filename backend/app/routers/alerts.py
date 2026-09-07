from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("")
def get_alerts(
    db: Session = Depends(get_db)
):
    alerts = (
        db.query(
            models.AlertModel
        )
        .order_by(
            models.AlertModel.id.desc()
        )
        .all()
    )

    return {
        "count": len(alerts),
        "alerts": alerts
    }


@router.get("/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = (
        db.query(
            models.AlertModel
        )
        .filter(
            models.AlertModel.id
            == alert_id
        )
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert