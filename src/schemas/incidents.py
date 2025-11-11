from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import IncidentSource, IncidentStatus


class IncidentCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=10_000)
    source: IncidentSource
    status: IncidentStatus | None = None


class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime
    updated_at: datetime


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus
