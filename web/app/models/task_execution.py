from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

from app.core.database import Base

if TYPE_CHECKING:
    from app.models import User, Day, Task


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doing_hours: Mapped[int] = mapped_column()
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    day_id: Mapped[int] = mapped_column(ForeignKey("days.id", ondelete="CASCADE"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    day: Mapped["Day"] = relationship("Day", back_populates="task_executions")
    owner: Mapped["User"] = relationship("User", back_populates="task_executions")
    task: Mapped["Task"] = relationship("Task", back_populates="task_executions")
