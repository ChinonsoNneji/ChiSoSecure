from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend.app import models


BRUTE_FORCE_THRESHOLD = 3
BRUTE_FORCE_WINDOW_MINUTES = 5


def analyze_event(event, db: Session):
    alerts = []

    # Rule 1: High severity event
    if event.severity == "high":
        alerts.append({
            "rule_name": "High Severity Event",
            "severity": "high",
            "message": (
                f"High severity security event detected "
                f"from {event.source_ip}"
            )
        })

    # Rule 2: Malware activity
    if event.event_type == "malware":
        alerts.append({
            "rule_name": "Malware Detection",
            "severity": "critical",
            "message": (
                f"Potential malware activity detected "
                f"from {event.source_ip}"
            )
        })

    # Rule 3: Privilege escalation
    if event.event_type == "privilege_escalation":
        alerts.append({
            "rule_name": "Privilege Escalation Detection",
            "severity": "critical",
            "message": (
                f"Privilege escalation activity detected "
                f"from {event.source_ip}"
            )
        })

    # Rule 4: Brute-force detection
    if event.event_type == "failed_login":
        cutoff_time = datetime.now(timezone.utc) - timedelta(
            minutes=BRUTE_FORCE_WINDOW_MINUTES
        )

        failed_login_count = (
            db.query(models.SecurityEventModel)
            .filter(
                models.SecurityEventModel.source_ip == event.source_ip,
                models.SecurityEventModel.event_type == "failed_login",
                models.SecurityEventModel.created_at >= cutoff_time
            )
            .count()
        )

        if failed_login_count >= BRUTE_FORCE_THRESHOLD:
            alerts.append({
                "rule_name": "Brute Force Detection",
                "severity": "high",
                "message": (
                    f"{failed_login_count} failed login attempts detected "
                    f"from {event.source_ip} within "
                    f"{BRUTE_FORCE_WINDOW_MINUTES} minutes"
                )
            })

    return alerts