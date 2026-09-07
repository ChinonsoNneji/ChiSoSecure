from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import Base, SessionLocal, engine
from backend.app.detection import analyze_event
from backend.app.response import execute_response_action
from backend.app.schemas import (
    IncidentCreate,
    IncidentStatusUpdate,
    ResponseActionCreate,
    SecurityEvent,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ChiSoSecure API",
    description=(
        "Cloud-native security detection and "
        "automated incident response platform."
    ),
    version="0.5.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def create_automatic_incident(
    alert,
    db: Session
):
    if alert.severity not in {
        "high",
        "critical"
    }:
        return None

    existing_incident = (
        db.query(models.IncidentModel)
        .filter(
            models.IncidentModel.alert_id
            == alert.id
        )
        .first()
    )

    if existing_incident:
        return existing_incident

    incident = models.IncidentModel(
        alert_id=alert.id,
        title=alert.rule_name,
        severity=alert.severity,
        status="open"
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@app.get("/")
def root():
    return {
        "service": "ChiSoSecure",
        "status": "operational",
        "version": "0.5.0"
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


# --------------------------------------------------
# RESPONSE ACTIONS
# --------------------------------------------------

@app.post("/response-actions")
def create_response_action(
    action: ResponseActionCreate,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(
            models.IncidentModel
        )
        .filter(
            models.IncidentModel.id
            == action.incident_id
        )
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    execution = execute_response_action(
        action.action_type,
        action.target
    )

    response_action = (
        models.ResponseActionModel(
            incident_id=action.incident_id,
            action_type=action.action_type,
            target=action.target,
            status=execution["status"],
            result=execution["result"]
        )
    )

    db.add(response_action)
    db.commit()
    db.refresh(response_action)

    return {
        "message": "Response action executed",
        "response_action": response_action
    }


@app.get("/response-actions")
def get_response_actions(
    db: Session = Depends(get_db)
):
    actions = (
        db.query(
            models.ResponseActionModel
        )
        .order_by(
            models.ResponseActionModel.id.desc()
        )
        .all()
    )

    return {
        "count": len(actions),
        "response_actions": actions
    }


@app.get(
    "/incidents/{incident_id}/response-actions"
)
def get_incident_response_actions(
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

    actions = (
        db.query(
            models.ResponseActionModel
        )
        .filter(
            models.ResponseActionModel.incident_id
            == incident_id
        )
        .order_by(
            models.ResponseActionModel.id.desc()
        )
        .all()
    )

    return {
        "incident_id": incident_id,
        "count": len(actions),
        "response_actions": actions
    }