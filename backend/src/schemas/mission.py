from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.cat import CatResponse
from schemas.target import TargetCreate, TargetResponse


class MissionBase(BaseModel):
    """Base mission schema."""


class MissionCreate(MissionBase):
    """Schema for creating a new mission."""

    targets: list[TargetCreate] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Mission targets"
        )

    @field_validator("targets")
    @classmethod
    def validate_targets_count(cls, v: list[TargetCreate]) -> list[TargetCreate]:
        """Validate targets count is between 1 and 3."""
        if not (1 <= len(v) <= 3):
            raise ValueError("Mission must have between 1 and 3 targets")
        return v


class MissionUpdate(BaseModel):
    """Schema for updating mission information."""

    cat_id: int | None = Field(default=None, description="Assign cat to mission")


class MissionResponse(MissionBase):
    """Schema for mission response."""

    id: int = Field(..., description="Mission's unique identifier")
    cat_id: int | None = Field(default=None, description="Assigned cat ID")
    is_complete: bool = Field(..., description="Mission completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: datetime | None = Field(
        default=None, description="Completion timestamp"
    )
    targets: list[TargetResponse] = Field(..., description="Mission targets")
    cat: CatResponse | None = Field(
        default=None, description="Assigned cat information"
    )

    model_config = ConfigDict(from_attributes=True)


class MissionListResponse(BaseModel):
    """Schema for listing missions."""

    missions: list[MissionResponse]
    total: int = Field(..., description="Total number of missions")
