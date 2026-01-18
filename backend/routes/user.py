# routes/user.py
from fastapi import APIRouter, Depends,Request
from dependencies.auth import inject_email
from controllers.user import register_user, login, logout, get_profile
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from utils.responses import ApiResponse
from schemas.user import UserOut


router = APIRouter()

@router.post("/register-user")
async def register(data: dict,db: AsyncSession = Depends(get_db)):
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
        secure=False,        # ❗ False on localhost
        samesite="lax",
        path="/"
    )
    resp.set_cookie(
        key="refreshToken",
        value=cookies["refreshToken"],
        httponly=True,
        secure=False,        # ❗ False on localhost
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