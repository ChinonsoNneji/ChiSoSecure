from sqlalchemy import Column, Integer, String
from backend.app.database import Base


class SecurityEventModel(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String, nullable=False)


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)
    rule_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)