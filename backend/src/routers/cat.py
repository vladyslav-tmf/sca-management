from fastapi import APIRouter, status, Query
from typing import Annotated

from db.dependencies import DBSession
from schemas.cat import CatCreate, CatListResponse, CatResponse, CatUpdate
from services.cat import (
    create_cat_service,
    delete_cat_service,
    get_cat_service,
    get_cats_service,
    update_cat_service,
)


router = APIRouter(prefix="/cats", tags=["cats"])


@router.post(
    path="/",
    response_model=CatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new spy cat",
    description="Create a new spy cat with breed validation using TheCatAPI"
)
async def create_cat(
    cat_data: CatCreate,
    session: DBSession
) -> CatResponse:
    """Create a new spy cat."""
    return await create_cat_service(session=session, cat_data=cat_data)


@router.get(
    path="/",
    response_model=CatListResponse,
    summary="List all spy cats",
    description="Get a paginated list of all spy cats"
)
async def get_cats(
    session: DBSession,
    skip: Annotated[int, Query(ge=0, description="Number of records to skip")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Number of records to return")
    ] = 100
) -> CatListResponse:
    """Get all spy cats with pagination."""
    return await get_cats_service(session=session, skip=skip, limit=limit)


@router.get(
    path="/{cat_id}",
    response_model=CatResponse,
    summary="Get a spy cat",
    description="Get a specific spy cat by ID"
)
async def get_cat(
    cat_id: int,
    session: DBSession
) -> CatResponse:
    """Get a spy cat by ID."""
    return await get_cat_service(session=session, cat_id=cat_id)


@router.patch(
    path="/{cat_id}",
    response_model=CatResponse,
    summary="Update spy cat information",
    description="Update spy cat information (currently only salary can be updated)"
)
async def update_cat(
    cat_id: int,
    cat_data: CatUpdate,
    session: DBSession
) -> CatResponse:
    """Update spy cat information."""
    return await update_cat_service(session=session, cat_id=cat_id, cat_data=cat_data)


@router.delete(
    path="/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a spy cat",
    description="Delete a spy cat (only if it has no active missions)"
)
async def delete_cat(
    cat_id: int,
    session: DBSession
) -> None:
    """Delete a spy cat."""
    await delete_cat_service(session=session, cat_id=cat_id)
