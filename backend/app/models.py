from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from backend.app.database import Base


class SecurityEventModel(Base):
    __tablename__ = "security_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    source_ip = Column(
        String,
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id = Column(
        Integer,
        nullable=False
    )

    rule_name = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class IncidentModel(Base):
    __tablename__ = "incidents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    alert_id = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="open"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )