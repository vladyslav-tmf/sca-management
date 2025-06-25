from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from repositories.cat import cat_has_active_mission, get_cat_by_id
from repositories.mission import (
    assign_cat_to_mission,
    create_mission,
    delete_mission, get_all_missions,
    get_mission_by_id, is_mission_assigned, update_mission_completion_status,
)
from repositories.target import get_target_by_id, update_target
from schemas.mission import MissionCreate, MissionListResponse, MissionResponse
from schemas.target import TargetResponse, TargetUpdate


async def create_mission_service(
    session: AsyncSession, mission_data: MissionCreate
) -> MissionResponse:
    """Create a new mission with targets."""
    try:
        mission = await create_mission(session=session, mission_data=mission_data)
        await session.commit()

        mission = await get_mission_by_id(session=session, mission_id=mission.id)
        return MissionResponse.model_validate(mission)
    except Exception as e:
        logger.error(f"Error creating mission: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create mission"
        )


async def get_mission_service(
    session: AsyncSession, mission_id: int
) -> MissionResponse:
    """Get mission by ID."""
    if not (mission := await get_mission_by_id(session=session, mission_id=mission_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )

    return MissionResponse.model_validate(mission)


async def get_missions_service(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> MissionListResponse:
    """Get all missions with pagination."""
    missions, total = await get_all_missions(session=session, skip=skip, limit=limit)

    return MissionListResponse(
        missions=[MissionResponse.model_validate(mission) for mission in missions],
        total=total
    )

async def assign_cat_to_mission_service(
    session: AsyncSession, mission_id: int, cat_id: int
) -> MissionResponse:
    """Assign a cat to a mission."""
    if not (mission := await get_mission_by_id(session=session, mission_id=mission_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )

    if mission.is_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign cat to completed mission"
        )

    if not await get_cat_by_id(session=session, cat_id=cat_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )

    if await cat_has_active_mission(session=session, cat_id=cat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cat already has an active mission"
        )

    try:
        updated_mission = await assign_cat_to_mission(
            session=session, mission=mission, cat_id=cat_id
        )
        await session.commit()

        updated_mission = await get_mission_by_id(
            session=session, mission_id=updated_mission.id
        )
        return MissionResponse.model_validate(updated_mission)
    except Exception as e:
        logger.error(f"Error assigning cat to mission: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign cat to mission"
        )

async def delete_mission_service(session: AsyncSession, mission_id: int) -> None:
    """Delete a mission if it's not assigned to a cat."""
    if not (mission := await get_mission_by_id(session=session, mission_id=mission_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )

    if await is_mission_assigned(session=session, mission_id=mission_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete mission that is assigned to a cat"
        )

    try:
        await delete_mission(session=session, mission=mission)
        await session.commit()
    except Exception as e:
        logger.error(f"Error deleting mission: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete mission"
        )


async def update_target_service(
    session: AsyncSession, target_id: int, target_data: TargetUpdate
) -> TargetResponse:
    """Update target information."""
    if not (target := await get_target_by_id(session=session, target_id=target_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target with id {target_id} not found"
        )

    mission = await get_mission_by_id(session=session, mission_id=target.mission_id)

    if target_data.notes is not None:
        if target.is_complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes for completed target"
            )
        if mission and mission.is_complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes for target in completed mission"
            )

    try:
        updated_target = await update_target(
            session=session, target=target, target_data=target_data
        )

        if target_data.is_complete is not None and mission:
            await update_mission_completion_status(session=session, mission=mission)

        await session.commit()
        return TargetResponse.model_validate(updated_target)
    except Exception as e:
        logger.error(f"Error updating target: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update target"
        )
