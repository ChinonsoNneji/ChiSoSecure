from pydantic import BaseModel


class SecurityEvent(BaseModel):
    source_ip: str
    event_type: str
    severity: str
    description: str