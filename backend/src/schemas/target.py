from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

class TargetBase(BaseModel):
    """Base target schema with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Target's name")
    country: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Target's country"
        )
    notes: str | None = Field(
        default=None,
        max_length=1000,
        description="Notes about the target"
        )

    @field_validator("name", "country")
    @classmethod
    def validate_strings(cls, v: str) -> str:
        """Validate string fields are not empty after stripping."""
        if not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, v: str | None) -> str | None:
        """Validate notes field."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class TargetCreate(TargetBase):
    """Schema for creating a new target."""


class TargetUpdate(BaseModel):
    """Schema for updating target information."""

    notes: str | None = Field(
        default=None, max_length=1000, description="Updated notes"
    )
    is_complete: bool | None = Field(
        default=None, description="Mark target as complete"
    )

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, v: str | None) -> str | None:
        """Validate notes field."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class TargetResponse(TargetBase):
    """Schema for target response."""

    id: int = Field(..., description="Target's unique identifier")
    mission_id: int = Field(..., description="Associated mission ID")
    is_complete: bool = Field(..., description="Target completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: datetime | None = Field(
        default=None, description="Completion timestamp"
    )

    model_config = ConfigDict(from_attributes=True)
