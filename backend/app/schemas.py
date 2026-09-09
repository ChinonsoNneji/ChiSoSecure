from typing import Literal

from pydantic import BaseModel, Field


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


class UserRegister(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserResponse(BaseModel):
    id: int
    username: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserRoleUpdate(BaseModel):
    role: Literal[
        "admin",
        "analyst",
        "viewer"
    ]