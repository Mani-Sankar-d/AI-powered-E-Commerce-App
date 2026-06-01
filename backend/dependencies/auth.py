# dependencies/auth.py
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import os
from backend.utils.errors import ApiError

async def inject_email(
    request: Request):
    access_token = request.cookies.get("accessToken")
    if not access_token:
        raise ApiError(401, "Unauthorized")
    try:
        decoded = jwt.decode(
            access_token,
            os.getenv("ACCESS_TOKEN_SECRET"),
            algorithms=["HS256"]
        )
    except jwt.PyJWTError:
        raise ApiError(status_code=401,message="Unauthorized")
    request.state.user_id = decoded["id"]
    request.state.user_email = decoded["email"]