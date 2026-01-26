# models/user.py
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base
import bcrypt

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    refresh_token: Mapped[str | None]

    orders = relationship("Order", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())
