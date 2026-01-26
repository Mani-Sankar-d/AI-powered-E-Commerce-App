# models/product.py
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]

    user_description: Mapped[str | None]
    description: Mapped[str | None]

    img_url: Mapped[str | None]

    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    owner = relationship("User")

    faiss_id: Mapped[int | None] = mapped_column(unique=True)
    indexed: Mapped[bool] = mapped_column(Boolean, default=False)

    status: Mapped[str] = mapped_column(default="PENDING")
    ml_error: Mapped[str | None]
    order_items = relationship("Order_item",back_populates="product")