from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.dependencies import get_db
from backend.app.schemas import (
    IncidentCreate,
    IncidentStatusUpdate,
)
from backend.app.security import (
    require_roles,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("")
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst"
        )
    )
):
    alert = (
        db.query(models.AlertModel)
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
        db.query(models.IncidentModel)
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


@router.get("")
def get_incidents(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst",
            "viewer"
        )
    )
):
    incidents = (
        db.query(models.IncidentModel)
        .order_by(
            models.IncidentModel.id.desc()
        )
        .all()
    )

    return {
        "count": len(incidents),
        "incidents": incidents
    }


@router.get("/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst",
            "viewer"
        )
    )
):
    incident = (
        db.query(models.IncidentModel)
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


@router.patch("/{incident_id}")
def update_incident_status(
    incident_id: int,
    update: IncidentStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "analyst"
        )
    )
):
    incident = (
        db.query(models.IncidentModel)
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


@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    )
):
    incident = (
        db.query(models.IncidentModel)
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