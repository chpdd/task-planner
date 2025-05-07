from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint, String, ForeignKey
from typing import TYPE_CHECKING
import datetime as dt

from src.database import Base
from src.config import settings

if TYPE_CHECKING:
    from src.models.user import User


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("1 <= interest AND interest <= 10", name="check_interest_range"),
        CheckConstraint("1 <= importance AND importance <= 10", name="check_importance_range"),
        CheckConstraint("1 <= work_hours AND work_hours <= 24", name="check_work_hours_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128))
    deadline: Mapped[dt.date] = mapped_column(nullable=True, default=None)
    interest: Mapped[int] = mapped_column(default=5)
    importance: Mapped[int] = mapped_column(default=5)
    work_hours: Mapped[int] = mapped_column(default=settings.default_task_work_hours)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship("User", back_populates="tasks")
