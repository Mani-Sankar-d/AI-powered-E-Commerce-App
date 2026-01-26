from backend.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey

class Order_item(Base):
    __tablename__="order_items"
    id:Mapped[int]=mapped_column(primary_key=True)
    order_id:Mapped[int]=mapped_column(ForeignKey("orders.id"))
    product_id:Mapped[int]=mapped_column(ForeignKey("products.id"))
    quantity:Mapped[int]
    price_snapshot:Mapped[int]
    
    order = relationship("Order",back_populates="items")
    product = relationship("Product",back_populates="order_items")