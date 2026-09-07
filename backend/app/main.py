from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.app.schemas import SecurityEvent
from backend.app.database import Base, engine, SessionLocal
from backend.app import models


Base.metadata.create_all(bind=engine)

app = FastAPI()


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
    db_event = models.SecurityEventModel(
        source_ip=event.source_ip,
        event_type=event.event_type,
        severity=event.severity,
        description=event.description
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {
        "message": "Security event stored",
        "event_id": db_event.id,
        "event": event
    }


@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(models.SecurityEventModel).all()

    return {
        "count": len(events),
        "events": events
    }