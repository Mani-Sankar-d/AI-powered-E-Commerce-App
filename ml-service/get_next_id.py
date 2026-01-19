# utils/get_next_id.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.counter import Counter

async def get_next_clip_id(db: AsyncSession) -> int:
    counter = await db.get(Counter, "clipId")

    if not counter:
        counter = Counter(name="clipId", value=1)
        db.add(counter)
    else:
        counter.value += 1

    await db.commit()
    return counter.value
