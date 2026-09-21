from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db
from backend.app.detection import analyze_event
from backend.app.schemas import SecurityEvent
from backend.app.services.api_keys import hash_api_key
from backend.app.services.incident_service import (
    create_automatic_incident,
)


router = APIRouter(
    prefix="/ingest",
    tags=["External API"],
)


def require_api_key(
    x_api_key: str = Header(
        ...,
        alias="X-API-Key"
    ),
    db: Session = Depends(get_db),
):
    key_hash = hash_api_key(x_api_key)

    api_key = (
        db.query(models.APIKeyModel)
        .filter(
            models.APIKeyModel.key_hash
            == key_hash,
            models.APIKeyModel.is_active.is_(
                True
            ),
        )
        .first()
    )

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key",
        )

    return api_key


@router.post("/events")
def ingest_event(
    event: SecurityEvent,
    db: Session = Depends(get_db),
    api_key=Depends(require_api_key),
):
    db_event = models.SecurityEventModel(
        source_ip=event.source_ip,
        event_type=event.event_type,
        severity=event.severity,
        description=event.description,
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
            message=alert["message"],
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
                "created_at": db_alert.created_at,
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
                    "created_at": incident.created_at,
                }
            )

    return {
        "message": (
            "External security event "
            "received and analyzed"
        ),
        "api_key_name": api_key.name,
        "event_id": db_event.id,
        "alerts_generated": len(
            stored_alerts
        ),
        "alerts": stored_alerts,
        "incidents_created": len(
            automatic_incidents
        ),
        "incidents": automatic_incidents,
    }
