from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from repositories.cat import (
    cat_has_active_mission,
    create_cat,
    delete_cat, get_all_cats,
    get_cat_by_id,
    update_cat,
)
from schemas.cat import CatCreate, CatListResponse, CatResponse, CatUpdate
from services.external_api import CatAPIService


async def create_cat_service(session: AsyncSession, cat_data: CatCreate) -> CatResponse:
    """Create a new cat with breed validation."""
    cat_api = CatAPIService()

    if not await cat_api.validate_breed(cat_data.breed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid cat breed: {cat_data.breed}"
        )

    try:
        cat = await create_cat(session=session, cat_data=cat_data)
        await session.commit()
        return CatResponse.model_validate(cat)
    except Exception as e:
        logger.error(f"Error creating cat: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create cat"
        )


async def get_cat_service(session: AsyncSession, cat_id: int) -> CatResponse:
    """Get cat by ID."""
    if not (cat := await get_cat_by_id(session=session, cat_id=cat_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )

    return CatResponse.model_validate(cat)


async def get_cats_service(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> CatListResponse:
    """Get all cats with pagination."""
    cats, total = await get_all_cats(session=session, skip=skip, limit=limit)

    return CatListResponse(
        cats=[CatResponse.model_validate(cat) for cat in cats],
        total=total
    )


async def update_cat_service(
    session: AsyncSession, cat_id: int, cat_data: CatUpdate
) -> CatResponse:
    """Update cat information."""
    if not (cat := await get_cat_by_id(session=session, cat_id=cat_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )

    try:
        updated_cat = await update_cat(session=session, cat=cat, cat_data=cat_data)
        await session.commit()
        return CatResponse.model_validate(updated_cat)
    except Exception as e:
        logger.error(f"Error updating cat: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update cat"
        )


async def delete_cat_service(session: AsyncSession, cat_id: int) -> None:
    """Delete a cat if it has no active missions."""
    if not (cat := await get_cat_by_id(session, cat_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )

    if await cat_has_active_mission(session=session, cat_id=cat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete cat with active missions"
        )

    try:
        await delete_cat(session=session, cat=cat)
        await session.commit()
    except Exception as e:
        logger.error(f"Error deleting cat: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete cat"
        )


async def check_cat_availability_service(session: AsyncSession, cat_id: int) -> bool:
    """Check if cat is available for new missions."""
    if not await get_cat_by_id(session=session, cat_id=cat_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )

    return not await cat_has_active_mission(session=session, cat_id=cat_id)
