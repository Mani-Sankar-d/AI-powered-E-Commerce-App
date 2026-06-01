from fastapi import APIRouter, Depends, UploadFile, File, Body,Request
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.dependencies.auth import inject_email
from backend.controllers.product import (
    get_products,
    add_product,
    get_product_by_id,
    get_products_by_name,
    get_all_products,
    buyproducts    
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
    product_name: str = Body(..., embed=True),  # this extracts the product_name key from incoming json and Body makes it extract from json otherwise it would expect product_name as query param
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
    description: str | None = Body(None),# None means optional
    image: UploadFile = File(...),# ... means required
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
@router.get("/id/{id}") # here id is declared as path param
async def product_by_id(
    id: int,  # normally this would be considered query param but since its mentioned in path so its a path param
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


@router.post("/buy")
async def buy(product_ids:dict ,request:Request, _:None = Depends(inject_email),db:AsyncSession=Depends(get_db)):
    return await buyproducts(product_ids["items"],request.state.user_id,db)