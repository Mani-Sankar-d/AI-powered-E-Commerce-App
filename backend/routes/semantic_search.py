from fastapi import APIRouter, Depends, UploadFile, File, Body,Request
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.dependencies.auth import inject_email
from backend.controllers.search import search_by_text,search_by_image
import io
router = APIRouter()



@router.post('/search_by_text')
async def text_query(
        text:str=Body(...),
        db:AsyncSession = Depends(get_db),
        _: None = Depends(inject_email)
):
    resp = await search_by_text(text,db)
    return resp
@router.post('/search_by_image')
async def image_query(
        image: UploadFile = File(...),
        db:AsyncSession = Depends(get_db),
        _: None = Depends(inject_email)
):
    contents = await image.read()
    stream = io.BytesIO(contents)
    resp = await search_by_image(stream,db)
    return resp