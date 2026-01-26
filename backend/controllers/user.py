# controllers/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from sqlalchemy.orm import selectinload
from models.user import User
from models.order import Order
from utils.responses import ApiResponse
from utils.errors import ApiError
from auth.tokens import generate_access_token, generate_refresh_token

COOKIE_OPTIONS = {
    "httponly": True,
    "secure": True
}

async def register_user(data: dict, db: AsyncSession):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        raise ApiError(400, "Invalid input")

    result = await db.execute(
        select(User).where(User.email == email)
    )
    if result.scalar_one_or_none():
        raise ApiError(401, "User exists already")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(
        username=username,
        email=email,
        password=hashed
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return ApiResponse(201, user, "User registered successfully")

async def login(data: dict, db: AsyncSession):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise ApiError(400, "Invalid input")

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise ApiError(400, "Register first then login")

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise ApiError(400, "Invalid credentials")

    access = generate_access_token(user)
    refresh = generate_refresh_token(user)

    user.refresh_token = refresh
    
    await db.commit()

    return {
        "response": ApiResponse(200, user, "User logged in successfully"),
        "cookies": {
            "accessToken": access,
            "refreshToken": refresh
        }
    }

async def get_profile(email: str, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == user.id)
    )
    orders = result.scalars().all()
    data = {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        "orders": [
            {
                "order_id": order.id,
                "total_amount": order.total_amount,
                "status": order.status,
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price_snapshot": item.price_snapshot,
                    }
                    for item in order.items
                ],
            }
            for order in orders
        ],
    }

    return ApiResponse(200, data, "Found successfully")

async def logout(email: str, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if user:
        user.refresh_token = None
        await db.commit()

    return ApiResponse(200, None, "Logged out successfully")

