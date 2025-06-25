from datetime import UTC, datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Mission, Target
from schemas.mission import MissionCreate


async def create_mission(session: AsyncSession, mission_data: MissionCreate) -> Mission:
    """Create a new mission with targets."""
    mission = Mission()
    session.add(mission)
    await session.flush()

    targets = [
        Target(
            mission_id=mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
        )
        for target_data in mission_data.targets
    ]

    session.add_all(targets)
    await session.flush()
    await session.refresh(mission)
    return mission


async def get_mission_by_id(session: AsyncSession, mission_id: int) -> Mission | None:
    """Get mission by ID with targets and cat."""
    result = await session.execute(
        select(Mission)
        .options(
            selectinload(Mission.targets),
            selectinload(Mission.cat)
        )
        .where(Mission.id == mission_id)
    )
    return result.scalar_one_or_none()


async def get_all_missions(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[list[Mission], int]:
    """Get all missions with pagination."""
    count_result = await session.execute(
        select(func.count(Mission.id))
    )
    total = count_result.scalar()

    result = await session.execute(
        select(Mission)
        .options(
            selectinload(Mission.targets),
            selectinload(Mission.cat)
        )
        .offset(skip)
        .limit(limit)
        .order_by(Mission.created_at.desc())
    )
    missions = result.scalars().all()

    return list(missions), total


async def assign_cat_to_mission(
    session: AsyncSession, mission: Mission, cat_id: int
) -> Mission:
    """Assign a cat to mission."""
    mission.cat_id = cat_id
    await session.flush()
    await session.refresh(mission)
    return mission


async def delete_mission(session: AsyncSession, mission: Mission) -> None:
    """Delete a mission."""
    await session.delete(mission)
    await session.flush()


async def is_mission_assigned(session: AsyncSession, mission_id: int) -> bool:
    """Check if mission is assigned to a cat."""
    result = await session.execute(
        select(Mission.cat_id).where(Mission.id == mission_id)
    )
    cat_id = result.scalar_one_or_none()
    return cat_id is not None


async def update_mission_completion_status(
    session: AsyncSession, mission: Mission
) -> Mission:
    """Update mission completion status based on targets."""
    result = await session.execute(
        select(func.count(Target.id))
        .where(Target.mission_id == mission.id)
        .where(Target.is_complete == False)
    )
    incomplete_targets = result.scalar()

    if incomplete_targets == 0 and not mission.is_complete:
        mission.is_complete = True
        mission.completed_at = datetime.now(UTC)
    elif incomplete_targets > 0 and mission.is_complete:
        mission.is_complete = False
        mission.completed_at = None

    await session.flush()
    await session.refresh(mission)
    return mission
