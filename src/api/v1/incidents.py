from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Query, status

from src.models.enums import IncidentStatus
from src.schemas.incidents import IncidentCreate, IncidentRead, IncidentStatusUpdate
from src.services.incidents import IncidentService

router = APIRouter(prefix="/incidents", tags=["incidents"], route_class=DishkaRoute)


@router.post(
    "",
    response_model=IncidentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an incident",
)
async def create_incident(
    service: FromDishka[IncidentService],
    payload: IncidentCreate,
) -> IncidentRead:
    incident = await service.create_incident(payload)
    return IncidentRead.model_validate(incident)


@router.get(
    "",
    response_model=list[IncidentRead],
    summary="Get a list of incidents",
)
async def list_incidents(
    service: FromDishka[IncidentService],
    status_filter: Annotated[IncidentStatus | None, Query(alias="status")] = None,
) -> list[IncidentRead]:
    incidents = await service.list_incidents(status=status_filter)
    return [IncidentRead.model_validate(incident) for incident in incidents]


@router.patch(
    "/{incident_id}",
    response_model=IncidentRead,
    summary="Update the status of an incident",
)
async def update_incident_status(
    service: FromDishka[IncidentService],
    incident_id: UUID,
    payload: IncidentStatusUpdate,
) -> IncidentRead:
    incident = await service.update_status(incident_id, payload.status)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return IncidentRead.model_validate(incident)
