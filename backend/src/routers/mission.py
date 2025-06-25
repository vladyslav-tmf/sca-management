from fastapi import APIRouter, status, Query
from typing import Annotated

from db.dependencies import DBSession
from schemas.mission import MissionCreate, MissionListResponse, MissionResponse
from services.mission import (
    assign_cat_to_mission_service,
    create_mission_service,
    delete_mission_service,
    get_mission_service,
    get_missions_service,
)


router = APIRouter(prefix="/missions", tags=["missions"])


@router.post(
    path="/",
    response_model=MissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new mission",
    description="Create a new mission with 1-3 targets"
)
async def create_mission(
    mission_data: MissionCreate,
    session: DBSession
) -> MissionResponse:
    """Create a new mission with targets."""
    return await create_mission_service(session=session, mission_data=mission_data)


@router.get(
    path="/",
    response_model=MissionListResponse,
    summary="List all missions",
    description=(
        "Get a paginated list of all missions with their targets and assigned cats"
    )
)
async def get_missions(
    session: DBSession,
    skip: Annotated[int, Query(ge=0, description="Number of records to skip")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Number of records to return")
    ] = 100
) -> MissionListResponse:
    """Get all missions with pagination."""
    return await get_missions_service(session=session, skip=skip, limit=limit)


@router.get(
    path="/{mission_id}",
    response_model=MissionResponse,
    summary="Get a mission",
    description="Get a specific mission by ID with targets and assigned cat information"
)
async def get_mission(
    mission_id: int,
    session: DBSession
) -> MissionResponse:
    """Get a mission by ID."""
    return await get_mission_service(session=session, mission_id=mission_id)


@router.patch(
    path="/{mission_id}/assign/{cat_id}",
    response_model=MissionResponse,
    summary="Assign cat to mission",
    description="Assign an available cat to a mission"
)
async def assign_cat_to_mission(
    mission_id: int,
    cat_id: int,
    session: DBSession
) -> MissionResponse:
    """Assign a cat to a mission."""
    return await assign_cat_to_mission_service(
        session=session, mission_id=mission_id, cat_id=cat_id
    )


@router.delete(
    path="/{mission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a mission",
    description="Delete a mission (only if it's not assigned to a cat)"
)
async def delete_mission(
    mission_id: int,
    session: DBSession
) -> None:
    """Delete a mission."""
    await delete_mission_service(session=session, mission_id=mission_id)
