# main.py
import uvicorn
from app import app
from db_init import init_db
import asyncio
@app.on_event("startup")
async def startup():
    await init_db()
# @app.on_event("startup")
# async def start_worker():
#     asyncio.create_task(worker_loop())
#     print("🚀 Worker task started")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
