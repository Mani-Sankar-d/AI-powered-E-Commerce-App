from fastapi import APIRouter, Depends, UploadFile, File, Body,Request
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from dependencies.auth import inject_email
from controllers.product import (
    get_products,
    add_product,
    get_product_by_id,
    get_products_by_name,
    get_all_products
)

router = APIRouter()

# GET /api/products
@router.get("/")
async def all_products(
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_products(db)


# POST /api/products/product-name
@router.post("/product-name")
async def products_by_name(
    product_name: str = Body(..., embed=True),
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    return await get_products(product_name, db)


# POST /api/products/new-product
@router.post("/new-product")
async def new_product(
    request:Request,
    name: str = Body(...),
    price: int = Body(...),
    description: str | None = Body(None),
    image: UploadFile = File(...),
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    return await add_product(
        db=db,
        image=image,
        name=name,
        price=price,
        owner_id=request.state.user_id,
        description=description,
    )


# GET /api/products/id/{id}
@router.get("/id/{id}")
async def product_by_id(
    id: int,
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    return await get_product_by_id(id, db)


# GET /api/products/name/{name}
@router.get("/name/{name}")
async def product_by_exact_name(
    name: str,
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    return await get_products_by_name(name, db)
