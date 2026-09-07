from sqlalchemy.orm import Session

from backend.app import models


def create_automatic_incident(
    alert: models.AlertModel,
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