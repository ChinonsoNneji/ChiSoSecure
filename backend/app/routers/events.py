from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db
from backend.app.detection import analyze_event
from backend.app.schemas import SecurityEvent
from backend.app.services.incident_service import (
    create_automatic_incident,
)


router = APIRouter(
    prefix="/events",
    tags=["Security Events"]
)


@router.post("")
def create_event(
    event: SecurityEvent,
    db: Session = Depends(get_db)
):
    db_event = models.SecurityEventModel(
        source_ip=event.source_ip,
        event_type=event.event_type,
        severity=event.severity,
        description=event.description
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    detected_alerts = analyze_event(
        db_event,
        db
    )

    stored_alerts = []
    automatic_incidents = []

    for alert in detected_alerts:
        db_alert = models.AlertModel(
            event_id=db_event.id,
            rule_name=alert["rule_name"],
            severity=alert["severity"],
            message=alert["message"]
        )

        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)

        stored_alerts.append(
            {
                "id": db_alert.id,
                "event_id": db_alert.event_id,
                "rule_name": db_alert.rule_name,
                "severity": db_alert.severity,
                "message": db_alert.message,
                "created_at": db_alert.created_at
            }
        )

        incident = create_automatic_incident(
            db_alert,
            db
        )

        if incident:
            automatic_incidents.append(
                {
                    "id": incident.id,
                    "alert_id": incident.alert_id,
                    "title": incident.title,
                    "severity": incident.severity,
                    "status": incident.status,
                    "created_at": incident.created_at
                }
            )

    return {
        "message": (
            "Security event stored and analyzed"
        ),
        "event_id": db_event.id,
        "alerts_generated": len(
            stored_alerts
        ),
        "alerts": stored_alerts,
        "incidents_created": len(
            automatic_incidents
        ),
        "incidents": automatic_incidents
    }


@router.get("")
def get_events(
    db: Session = Depends(get_db)
):
    events = (
        db.query(
            models.SecurityEventModel
        )
        .order_by(
            models.SecurityEventModel.id.desc()
        )
        .all()
    )

    return {
        "count": len(events),
        "events": events
    }


@router.get("/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = (
        db.query(
            models.SecurityEventModel
        )
        .filter(
            models.SecurityEventModel.id
            == event_id
        )
        .first()
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Security event not found"
        )

    return event