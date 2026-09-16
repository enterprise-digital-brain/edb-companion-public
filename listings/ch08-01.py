from pydantic import BaseModel, Field
from typing import Literal

class AccessRequest(BaseModel):
    user_id: str
    resource_id: str
    permission: Literal["read", "operate"]
    expires_minutes: int = Field(ge=15, le=480)
    incident_id: str
    idempotency_key: str

class AccessResult(BaseModel):
    request_id: str
    status: Literal["granted", "pending_approval", "denied"]
    expires_at: str | None
