from typing import Literal

from pydantic import BaseModel


class SecurityEvent(BaseModel):
    source_ip: str
    event_type: str
    severity: str
    description: str


class IncidentCreate(BaseModel):
    alert_id: int
    title: str
    severity: str


class IncidentStatusUpdate(BaseModel):
    status: Literal[
        "open",
        "investigating",
        "resolved"
    ]


class ResponseActionCreate(BaseModel):
    incident_id: int
    action_type: Literal[
        "block_ip",
        "isolate_host",
        "disable_account"
    ]
    target: str