# dependencies/auth.py
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import os

from backend.db import get_db
from backend.models.user import User
from backend.utils.errors import ApiError
from backend.auth.tokens import generate_access_token, generate_refresh_token

async def inject_email(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    access_token = request.cookies.get("accessToken")
    refresh_token = request.cookies.get("refreshToken")
    if access_token:
        try:
            decoded = jwt.decode(
                access_token,
                os.getenv("ACCESS_TOKEN_SECRET"),
                algorithms=["HS256"]
            )
            request.state.user_id = decoded["id"]
            request.state.user_email = decoded["email"]
            return
        except jwt.PyJWTError:
            pass

    if not refresh_token:
        print("Missing refresh token")
        raise ApiError(401, "Login first")

    try:
        decoded = jwt.decode(
            refresh_token,
            os.getenv("REFRESH_TOKEN_SECRET"),
            algorithms=["HS256"]
        )
    except jwt.PyJWTError:
        raise ApiError(401, "Invalid refresh token")

    user = await db.get(User, decoded["id"])
    if not user or user.refresh_token != refresh_token:
        raise ApiError(401, "Refresh token revoked")

    new_access = generate_access_token(user)
    new_refresh = generate_refresh_token(user)

    user.refresh_token = new_refresh
    await db.commit()

    request.state.user_id = user.id
    request.state.user_email = user.email

    request.state.set_cookies = {
        "accessToken": new_access,
        "refreshToken": new_refresh
    }
