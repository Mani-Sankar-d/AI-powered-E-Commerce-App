# app.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from routes.user import router as user_router
from routes.product import router as product_router
from routes.home import router as home_router
from utils.errors import ApiError
from db_init import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-powered-e-commerce-app-production.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def f():
    return {"ok": True}
@app.get("/health")
async def health():
    return {"ok": True}
# app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(user_router, prefix="/api/users")
app.include_router(product_router, prefix="/api/products")
app.include_router(home_router, prefix="/api")

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )
