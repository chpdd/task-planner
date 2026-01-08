from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from app.core.database import Base

if TYPE_CHECKING:
    from app.models import Task, Day, TaskExecution, FailedTask, ManualDay


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan",
                                               passive_deletes=True)
    days: Mapped[list["Day"]] = relationship("Day", back_populates="owner", cascade="all, delete-orphan",
                                             passive_deletes=True)
    task_executions: Mapped[list["TaskExecution"]] = relationship("TaskExecution", back_populates="owner",
                                                                  cascade="all, delete-orphan", passive_deletes=True)
    failed_tasks: Mapped[list["FailedTask"]] = relationship("FailedTask", back_populates="owner",
                                                            cascade="all, delete-orphan", passive_deletes=True)
    manual_days: Mapped[list["ManualDay"]] = relationship("ManualDay", back_populates="owner",
                                                          cascade="all, delete-orphan", passive_deletes=True)
