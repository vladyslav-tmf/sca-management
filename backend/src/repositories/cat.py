from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Cat, Mission
from schemas.cat import CatCreate, CatUpdate


async def create_cat(session: AsyncSession, cat_data: CatCreate) -> Cat:
    """Create a new cat."""
    cat = Cat(
        name=cat_data.name,
        years_of_experience=cat_data.years_of_experience,
        breed=cat_data.breed,
        salary=cat_data.salary,
    )
    session.add(cat)
    await session.flush()
    await session.refresh(cat)
    return cat


async def get_cat_by_id(session: AsyncSession, cat_id: int) -> Cat | None:
    """Get cat by ID."""
    result = await session.execute(
        select(Cat).where(Cat.id == cat_id)
    )
    return result.scalar_one_or_none()


async def get_all_cats(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[list[Cat], int]:
    """Get all cats with pagination."""
    count_result = await session.execute(
        select(func.count(Cat.id))
    )
    total = count_result.scalar()

    result = await session.execute(
        select(Cat)
        .offset(skip)
        .limit(limit)
        .order_by(Cat.created_at.desc())
    )
    cats = result.scalars().all()

    return list(cats), total


async def update_cat(session: AsyncSession, cat: Cat, cat_data: CatUpdate) -> Cat:
    """Update cat information."""
    if cat_data.salary is not None:
        cat.salary = cat_data.salary

    await session.flush()
    await session.refresh(cat)
    return cat


async def delete_cat(session: AsyncSession, cat: Cat) -> None:
    """Delete a cat."""
    await session.delete(cat)
    await session.flush()


async def get_cats_by_breed(session: AsyncSession, breed: str) -> list[Cat]:
    """Get cats by breed."""
    result = await session.execute(
        select(Cat).where(Cat.breed == breed)
    )
    return list(result.scalars().all())


async def cat_has_active_mission(session: AsyncSession, cat_id: int) -> bool:
    """Check if cat has an active mission."""
    result = await session.execute(
        select(func.count(Mission.id))
        .where(Mission.cat_id == cat_id)
        .where(Mission.is_complete == False)
    )
    return result.scalar() > 0
