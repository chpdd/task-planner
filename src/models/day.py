from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint, ForeignKey
from typing import TYPE_CHECKING
import datetime as dt

from src.database import Base
from src.config import settings

if TYPE_CHECKING:
    from src.models.user import User


class Day(Base):
    __tablename__ = "days"
    __table_args__ = (
        CheckConstraint("1 <= interest AND interest <= 10", name="check_work_hours_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[dt.date] = mapped_column()
    work_hours: Mapped[int]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship("User", back_populates="days")
