from dataclasses import dataclass
from uuid import UUID

import structlog

from src.models.enums import IncidentStatus
from src.models.incidents import Incident
from src.repositories.incidents import IncidentRepository
from src.schemas.incidents import IncidentCreate

logger = structlog.get_logger(__name__)


@dataclass(slots=True)
class IncidentService:
    repository: IncidentRepository

    async def create_incident(self, payload: IncidentCreate) -> Incident:
        status = payload.status or IncidentStatus.NEW
        incident = await self.repository.create(
            description=payload.description,
            source=payload.source,
            status=status,
        )

        logger.info(
            "incident_created",
            incident_id=str(incident.id),
            status=incident.status.value,
            source=incident.source.value,
        )
        return incident

    async def list_incidents(
        self,
        status: IncidentStatus | None = None,
    ) -> list[Incident]:
        incidents = await self.repository.list(status=status)
        return list(incidents)

    async def update_status(
        self,
        incident_id: UUID,
        status: IncidentStatus,
    ) -> Incident | None:
        incident = await self.repository.update_status(incident_id, status)
        if incident is None:
            return None

        logger.info(
            "incident_status_updated",
            incident_id=str(incident.id),
            status=incident.status.value,
        )
        return incident
