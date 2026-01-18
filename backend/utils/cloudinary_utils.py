# cloudinary_utils.py
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

async def upload_on_cloudinary(buffer: bytes, folder="products"):
    result = cloudinary.uploader.upload(
        buffer,
        folder=folder
    )
    return result
