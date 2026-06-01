# routes/user.py
from fastapi import APIRouter, Depends,Request
import jwt
import os
from backend.utils.errors import ApiError
from backend.auth.tokens import generate_access_token,generate_refresh_token
from backend.dependencies.auth import inject_email
from backend.controllers.user import register_user, login, logout, get_profile
from backend.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from backend.utils.responses import ApiResponse
from backend.schemas.user import UserOut
from backend.models.user import User

router = APIRouter()

@router.post("/register-user")
async def register(data: dict,db: AsyncSession = Depends(get_db)):
    # print("registter hit")
    return await register_user(data,db)

@router.post("/login")
async def login_route(
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    result = await login(data, db)

    response_data: ApiResponse = result["response"]
    cookies = result["cookies"]

    resp = JSONResponse(
        content={
            "success": True,
            "status": 200,
            "message": "User logged in successfully",
            "data": UserOut.model_validate(
                response_data.data
            ).model_dump()
        }
    )

    # IMPORTANT: dev settings
    a=cookies["accessToken"]
    r=cookies["refreshToken"]
    # print(f"setting accessToken and refreshToken {a} {r}")
    resp.set_cookie(
        key="accessToken",
        value=cookies["accessToken"],
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    resp.set_cookie(
        key="refreshToken",
        value=cookies["refreshToken"],
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )

    return resp

@router.post("/logout")
async def logout_route(
    request: Request,
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    # revoke refresh token in DB
    await logout(request.state.user_email, db)

    resp = JSONResponse(
        content=ApiResponse(200, None, "Logged out successfully").dict()
    )

    # DELETE cookies (IMPORTANT)
    resp.delete_cookie(
        key="accessToken",
        httponly=True,
        secure=False,   # must match how it was set
        samesite="lax"
    )
    resp.delete_cookie(
        key="refreshToken",
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return resp

@router.get("/get-profile")
async def profile(
    request: Request,
    _: None = Depends(inject_email),
    db: AsyncSession = Depends(get_db),
):
    return await get_profile(request.state.user_email, db)

@router.post("/refresh")
async def refresh(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get("refreshToken")
    if not refresh_token:
        print("Missing refresh token")
        raise ApiError(401, "Login first")
    try:
        # print(f"refresh_token:{refresh_token}")
        decoded = jwt.decode(
            refresh_token,
            os.getenv("REFRESH_TOKEN_SECRET"),
            algorithms=["HS256"]
        )
    except Exception as e:
        # print(type(e))
        # print(e)
        raise ApiError(401, "Invalid refresh token")

    user = await db.get(User, decoded["id"])
    if not user:
        raise ApiError(401, "User not found")
    if user.refresh_token != refresh_token:
        raise ApiError(401, "Refresh token revoked")
    new_access = generate_access_token(user)
    new_refresh = generate_refresh_token(user)
    user.refresh_token = new_refresh
    await db.commit()
    resp = JSONResponse(
        content=ApiResponse(200, None, "Refreshed successfully").dict()
    )
    resp.set_cookie(
        key="accessToken",
        value=new_access,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    resp.set_cookie(
        key="refreshToken",
        value=new_refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return resp