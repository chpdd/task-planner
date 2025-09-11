from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING
import datetime as dt

from app.database import Base
from app.config import settings

if TYPE_CHECKING:
    from app.models import User


class ManualDay(Base):
    __tablename__ = "manual_days"
    __table_args__ = (
        CheckConstraint("0 <= work_hours AND work_hours <= 24", name="check_work_hours_range"),
        UniqueConstraint("date", "owner_id", name="unique_date_for_user_manual_days")
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[dt.date] = mapped_column()
    work_hours: Mapped[int] = mapped_column(default=settings.default_day_work_hours)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    owner: Mapped["User"] = relationship("User", back_populates="manual_days")
