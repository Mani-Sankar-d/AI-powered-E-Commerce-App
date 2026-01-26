# db.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


#engine is creator of connections to db server to communicate these are limited pool pre ping is to prevent giving away dead connections to sesssions
#session is a unit of work like when a request wants db it gets a session then from engine if any connection is free the session uses and return the connection after use
#get db generates new session for each request then close after use 