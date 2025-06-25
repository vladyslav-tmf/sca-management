from fastapi import APIRouter

from db.dependencies import DBSession
from schemas.target import TargetResponse, TargetUpdate
from services.mission import update_target_service


router = APIRouter(prefix="/targets", tags=["targets"])


@router.patch(
    path="/{target_id}",
    response_model=TargetResponse,
    summary="Update target information",
    description="Update target notes and/or completion status"
)
async def update_target(
    target_id: int,
    target_data: TargetUpdate,
    session: DBSession
) -> TargetResponse:
    """Update target information."""
    return await update_target_service(
        session=session, target_id=target_id, target_data=target_data
    )
