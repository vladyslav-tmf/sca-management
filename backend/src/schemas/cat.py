from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CatBase(BaseModel):
    """Base cat schema with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Cat's name")
    years_of_experience: int = Field(
        ...,
        ge=0,
        le=50,
        description="Years of experience"
        )
    breed: str = Field(..., min_length=1, max_length=100, description="Cat's breed")
    salary: Decimal = Field(..., gt=0, decimal_places=2, description="Cat's salary")

    @field_validator("name", "breed")
    @classmethod
    def validate_strings(cls, v: str) -> str:
        """Validate string fields are not empty after stripping."""
        if not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class CatCreate(CatBase):
    """Schema for creating a new cat."""


class CatUpdate(BaseModel):
    """Schema for updating cat information."""

    salary: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
        description="Updated salary"
        )


class CatResponse(CatBase):
    """Schema for cat response."""

    id: int = Field(..., description="Cat's unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class CatListResponse(BaseModel):
    """Schema for listing cats."""

    cats: list[CatResponse]
    total: int = Field(..., description="Total number of cats")
