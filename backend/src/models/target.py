from datetime import datetime

from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class Target(Base):
    """Target model."""

    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    country: Mapped[str] = mapped_column(index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_complete: Mapped[bool] = mapped_column(default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    mission_id: Mapped[int] = mapped_column(
        ForeignKey(column="missions.id", ondelete="CASCADE"),
        index=True
    )

    # Relationships
    mission: Mapped["Mission"] = relationship(
        argument="Mission",
        back_populates="targets"
    )

    # Table constraints
    __table_args__ = (
        UniqueConstraint("mission_id", "name", name="uq_target_mission_name"),
    )

    def __repr__(self) -> str:
        return (
            f"<Target(id={self.id}, name='{self.name}', country='{self.country}', "
            f"is_complete={self.is_complete})>"
        )
