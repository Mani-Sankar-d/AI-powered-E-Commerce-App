# db_init.py
from db import engine
from models.base import Base

# IMPORTANT: import all models so they register with Base
from models.user import User
from models.product import Product
from models.order import Order
from models.counter import Counter

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
