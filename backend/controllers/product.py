# controllers/product.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile
from utils.errors import ApiError
from utils.responses import ApiResponse
from models.product import Product
from utils.cloudinary_utils import upload_on_cloudinary

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
