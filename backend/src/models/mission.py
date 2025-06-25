from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class Mission(Base):
    """Mission model."""

    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_complete: Mapped[bool] = mapped_column(default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    cat_id: Mapped[int | None] = mapped_column(
        ForeignKey(column="cats.id", ondelete="SET NULL"),
        index=True
    )

    # Relationships
    cat: Mapped[Optional["Cat"]] = relationship(
        argument="Cat",
        back_populates="missions"
    )
    targets: Mapped[list["Target"]] = relationship(
        argument="Target",
        back_populates="mission",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Mission(id={self.id}, cat_id={self.cat_id}, "
            f"is_complete={self.is_complete})>"
        )
