from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.enums import IncidentSource, IncidentStatus
from src.models.incidents import Incident


@dataclass(slots=True)
class IncidentRepository:
    session: AsyncSession

    async def create(
        self,
        *,
        description: str,
        source: IncidentSource,
        status: IncidentStatus,
    ) -> Incident:
        incident = Incident(description=description, source=source, status=status)
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def list(self, status: IncidentStatus | None = None) -> Sequence[Incident]:
        stmt: Select[tuple[Incident]] = select(Incident).order_by(
            Incident.created_at.desc(),
        )
        if status is not None:
            stmt = stmt.where(Incident.status == status)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get(self, incident_id: UUID) -> Incident | None:
        stmt = select(Incident).where(Incident.id == incident_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(
        self,
        incident_id: UUID,
        status: IncidentStatus,
    ) -> Incident | None:
        incident = await self.get(incident_id)
        if incident is None:
            return None

        incident.status = status
        incident.updated_at = datetime.now(UTC)

        await self.session.commit()
        await self.session.refresh(incident)
        return incident
