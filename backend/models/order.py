from backend.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped,relationship
from datetime import datetime
from sqlalchemy import DateTime, func, ForeignKey

class Order(Base):
    __tablename__="orders"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_amount:Mapped[int]
    status:Mapped[str]
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    user = relationship("User",back_populates="orders")
    items=relationship("Order_item",back_populates="order")