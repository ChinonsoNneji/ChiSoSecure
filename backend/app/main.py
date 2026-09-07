from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import Base, SessionLocal, engine
from backend.app.detection import analyze_event
from backend.app.schemas import (
    IncidentCreate,
    IncidentStatusUpdate,
    SecurityEvent,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ChiSoSecure API",
    description=(
        "Cloud-native security detection and "
        "incident response platform."
    ),
    version="0.3.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get("/")
def root():
    return {
        "service": "ChiSoSecure",
        "status": "operational",
        "version": "0.3.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# SECURITY EVENTS
# --------------------------------------------------

@app.post("/events")
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

    return {
        "message": (
            "Security event stored and analyzed"
        ),
        "event_id": db_event.id,
        "event": {
            "id": db_event.id,
            "source_ip": db_event.source_ip,
            "event_type": db_event.event_type,
            "severity": db_event.severity,
            "description": db_event.description,
            "created_at": db_event.created_at
        },
        "alerts_generated": len(
            stored_alerts
        ),
        "alerts": stored_alerts
    }


@app.get("/events")
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


@app.get("/events/{event_id}")
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


# --------------------------------------------------
# ALERTS
# --------------------------------------------------

@app.get("/alerts")
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


@app.get("/alerts/{alert_id}")
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


# --------------------------------------------------
# INCIDENTS
# --------------------------------------------------

@app.post("/incidents")
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):

    alert = (
        db.query(
            models.AlertModel
        )
        .filter(
            models.AlertModel.id
            == incident.alert_id
        )
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    existing_incident = (
        db.query(
            models.IncidentModel
        )
        .filter(
            models.IncidentModel.alert_id
            == incident.alert_id
        )
        .first()
    )

    if existing_incident:
        raise HTTPException(
            status_code=409,
            detail=(
                "An incident already exists "
                "for this alert"
            )
        )

    db_incident = models.IncidentModel(
        alert_id=incident.alert_id,
        title=incident.title,
        severity=incident.severity,
        status="open"
    )

    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    return {
        "message": "Incident created",
        "incident": db_incident
    }


@app.get("/incidents")
def get_incidents(
    db: Session = Depends(get_db)
):

    incidents = (
        db.query(
            models.IncidentModel
        )
        .order_by(
            models.IncidentModel.id.desc()
        )
        .all()
    )

    return {
        "count": len(incidents),
        "incidents": incidents
    }


@app.get("/incidents/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(
            models.IncidentModel
        )
        .filter(
            models.IncidentModel.id
            == incident_id
        )
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@app.patch("/incidents/{incident_id}")
def update_incident_status(
    incident_id: int,
    update: IncidentStatusUpdate,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(
            models.IncidentModel
        )
        .filter(
            models.IncidentModel.id
            == incident_id
        )
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident.status = update.status

    db.commit()
    db.refresh(incident)

    return {
        "message": "Incident status updated",
        "incident": incident
    }


@app.delete("/incidents/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(
            models.IncidentModel
        )
        .filter(
            models.IncidentModel.id
            == incident_id
        )
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)
    db.commit()

    return {
        "message": (
            f"Incident {incident_id} deleted"
        )
    }