# main.py
import uvicorn
from backend.app import app
import asyncio


if __name__ == "__main__":
    uvicorn.run("backend.app:app", reload=True)
