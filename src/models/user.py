from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint, String
from typing import TYPE_CHECKING

from src.database import Base

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.day import Day


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")
    days: Mapped[list["Day"]] = relationship("Day", back_populates="owner")
