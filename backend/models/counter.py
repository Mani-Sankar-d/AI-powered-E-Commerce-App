# models/counter.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from backend.models.base import Base

class Counter(Base):
    __tablename__ = "counters"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, default=0)
