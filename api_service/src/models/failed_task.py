from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint, String, ForeignKey, UniqueConstraint, Index
from typing import TYPE_CHECKING
import datetime as dt

from src.database import Base
from src.config import settings

if TYPE_CHECKING:
    from src.models import User, Task, Calendar


class FailedTask(Base):
    __tablename__ = "failed_tasks"
    __table_args__ = (
        Index("owner_id_task_id_index", "owner_id", "task_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True, unique=True)

    owner: Mapped["User"] = relationship("User", back_populates="failed_tasks")
    task: Mapped["Task"] = relationship("Task")
