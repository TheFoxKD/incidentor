from uuid import UUID

from sqlalchemy import Enum, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimestampedBase
from .enums import IncidentSource, IncidentStatus


class Incident(TimestampedBase):
    __tablename__ = "incidents"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, name="incident_status"),
        nullable=False,
        default=IncidentStatus.NEW,
    )
    source: Mapped[IncidentSource] = mapped_column(
        Enum(IncidentSource, name="incident_source"),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"Incident(id={self.id!s}, status={self.status}, source={self.source})"
