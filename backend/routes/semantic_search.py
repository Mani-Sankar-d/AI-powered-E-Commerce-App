from fastapi import APIRouter, Depends, UploadFile, File, Body,Request
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.dependencies.auth import inject_email
from backend.controllers.search import search_by_text,search_by_image

router = APIRouter()

@router.post('/search_by_text')
async def text_query(
        text:str=Body(...),
        db:AsyncSession = Depends(get_db),
        _: None = Depends(inject_email)
):
    return search_by_text(text)

@router.post('/search_by_image')
async def text_query(
        image: UploadFile = File(...),
        db:AsyncSession = Depends(get_db),
        _: None = Depends(inject_email)
):
    return search_by_image(image)