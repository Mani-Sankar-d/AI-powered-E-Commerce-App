# main.py
import uvicorn
from app import app
from db_init import init_db
import asyncio
@app.on_event("startup")
async def startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
