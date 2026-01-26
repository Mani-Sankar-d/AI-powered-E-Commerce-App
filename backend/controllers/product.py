# controllers/product.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile
from backend.utils.errors import ApiError
from backend.utils.responses import ApiResponse
from backend.models.product import Product
from backend.utils.cloudinary_utils import upload_on_cloudinary
from backend.db import get_db
from fastapi import Depends
from sqlalchemy import select
from backend.models.order import Order
from backend.models.order_items import Order_item
# GET /name/{name}
async def get_products_by_name(name: str, db: AsyncSession):
    result = await db.execute(
        select(Product).where(Product.name == name)
    )
    products = result.scalars().all()
    return ApiResponse(200, f"Got all products named {name}", products)

# GET /
async def get_all_products(db: AsyncSession):
    result = await db.execute(
        select(Product).order_by(Product.id.desc())
    )
    products = result.scalars().all()
    return ApiResponse(200, "Got all products", products)

# GET /id/{id}
async def get_product_by_id(id: int, db: AsyncSession):
    product = await db.get(Product, id)
    if not product:
        raise ApiError(400, "Not found")
    return ApiResponse(200, "Got specified product", product)

# POST /product-name
async def get_products(product_name: str, db: AsyncSession):
    if not product_name:
        raise ApiError(400, "Product field empty")

    result = await db.execute(
        select(Product).where(Product.name == product_name)
    )
    products = result.scalars().all()

    if not products:
        raise ApiError(400, "No such product")

    return ApiResponse(200, "Found", products)

# POST /new-product
async def add_product(
    *,
    db: AsyncSession,
    image: UploadFile,
    name: str,
    price: int,
    owner_id: int,
    description: str | None = None
):
    if not image:
        raise ApiError(400, "Image is required")

    buffer = await image.read()
    result = await upload_on_cloudinary(buffer)
    image_url = result["secure_url"]

    product = Product(
        name=name,
        price=price,
        description=description,
        owner_id=owner_id,
        img_url=image_url,
        indexed=False,
        status="PENDING"
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return ApiResponse(201, product, "Product created successfully")

async def buyproducts(product_ids:dict, user_Id:int, db:AsyncSession):    
    total=0
    product_list = {}
    for pid,quantity in product_ids.items():
        pid,quantity = int(pid),int(quantity)
        if quantity<=0:
            continue
        stmt = select(Product).where(Product.id==pid)
        product = await db.execute(stmt)
        product = product.scalars().first()
        if(product is None):
            continue
        product_list[pid] = product
        total+=product.price * quantity
    
    neworder = Order(user_id=user_Id,total_amount=total,status="pending")
    db.add(neworder)
    await db.flush()

    for pid,quantity in product_ids.items():
        pid,quantity = int(pid),int(quantity)
        if quantity<=0 or pid not in product_list:
            continue
        product = product_list[pid]
        new_order_item = Order_item(order_id=neworder.id, product_id=pid,quantity=quantity,price_snapshot=product.price)
        db.add(new_order_item)
    await db.commit()