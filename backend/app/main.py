from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.app.schemas import SecurityEvent
from backend.app.database import Base, engine, SessionLocal
from backend.app import models
from backend.app.detection import analyze_event


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChiSoSecure API",
    description="Security event detection and automated incident response platform.",
    version="0.1.0"
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
        "status": "operational"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/events")
def create_event(
    event: SecurityEvent,
    db: Session = Depends(get_db)
):
    # Store incoming security event
    db_event = models.SecurityEventModel(
        source_ip=event.source_ip,
        event_type=event.event_type,
        severity=event.severity,
        description=event.description
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Analyze the event.
    # We pass the database session so detection rules
    # can examine previously stored events.
    detected_alerts = analyze_event(db_event, db)

    stored_alerts = []

    # Store generated alerts
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

        stored_alerts.append({
            "id": db_alert.id,
            "event_id": db_alert.event_id,
            "rule_name": db_alert.rule_name,
            "severity": db_alert.severity,
            "message": db_alert.message
        })

    return {
        "message": "Security event stored and analyzed",
        "event_id": db_event.id,
        "event": {
            "source_ip": db_event.source_ip,
            "event_type": db_event.event_type,
            "severity": db_event.severity,
            "description": db_event.description
        },
        "alerts_generated": len(stored_alerts),
        "alerts": stored_alerts
    }


@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(models.SecurityEventModel).all()

    return {
        "count": len(events),
        "events": events
    }


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(models.AlertModel).all()

    return {
        "count": len(alerts),
        "alerts": alerts
    }