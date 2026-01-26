# db_init.py
from backend.db import engine
from backend.models.base import Base
from sqlalchemy.ext import asyncio
# IMPORTANT: import all models so they register with Base
from backend.models.user import User
from backend.models.product import Product
from backend.models.order import Order
from backend.models.counter import Counter
from backend.models.order_items import Order_item

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)