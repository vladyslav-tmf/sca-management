from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class Cat(Base):
    """Spy Cat model."""

    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    years_of_experience: Mapped[int]
    breed: Mapped[str] = mapped_column(index=True)
    salary: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    missions: Mapped[list["Mission"]] = relationship(
        argument="Mission",
        back_populates="cat",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cat(id={self.id}, name='{self.name}', breed='{self.breed}')>"
