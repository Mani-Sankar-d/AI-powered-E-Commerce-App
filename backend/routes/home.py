# routes/home.py
from fastapi import APIRouter, Depends
from dependencies.auth import inject_email
from controllers.product import get_all_products
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
router = APIRouter()

@router.get("/")
async def home(
    _ = Depends(inject_email),db:AsyncSession=Depends(get_db)):
    return await get_all_products(db)
