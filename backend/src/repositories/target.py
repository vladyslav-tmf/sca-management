from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Target
from schemas.target import TargetUpdate


async def get_target_by_id(session: AsyncSession, target_id: int) -> Target | None:
    """Get target by ID."""
    result = await session.execute(
        select(Target).where(Target.id == target_id)
    )
    return result.scalar_one_or_none()


async def update_target(
    session: AsyncSession, target: Target, target_data: TargetUpdate
) -> Target:
    """Update target information."""
    if target_data.notes is not None:
        target.notes = target_data.notes

    if target_data.is_complete is not None:
        target.is_complete = target_data.is_complete
        if target_data.is_complete:
            target.completed_at = datetime.now(UTC)
        else:
            target.completed_at = None

    await session.flush()
    await session.refresh(target)
    return target


async def get_mission_targets(session: AsyncSession, mission_id: int) -> list[Target]:
    """Get all targets for a mission."""
    result = await session.execute(
        select(Target).where(Target.mission_id == mission_id)
    )
    return list(result.scalars().all())
