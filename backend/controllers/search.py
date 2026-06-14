import warnings
warnings.filterwarnings("ignore")
import torch
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import numpy as np
import pickle
import faiss
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.product import Product
import os
INDEX_PATH = os.getenv("INDEX_PATH")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

model.eval()
def image_to_embedding(stream):
    img = Image.open(stream).convert("RGB")
    inputs = processor(
        images=img,
        return_tensors="pt"
    ).to(device)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    embedding = embedding.cpu().numpy()[0]
    return embedding

def text_to_embedding(text):
    # print("text embedding generation initiating")
    inputs = processor(
        text=[text],return_tensors='pt',padding=True,truncation=True
    ).to(device)
    with torch.no_grad():
        embedding = model.get_text_features(**inputs)
    # print("text embedding generation completed")
    embedding = embedding.cpu().numpy()[0]
    return embedding


async def search_products(query_vec,
                          db: AsyncSession,
                          index_path=INDEX_PATH):
    query_vec = query_vec / np.linalg.norm(query_vec)

    index = faiss.read_index(index_path)

    D, I = index.search(query_vec.reshape(1, -1), 25)

    product_ids = [
        int(pid)
        for pid in I[0]
        if pid != -1
    ]

    result = await db.execute(
        select(Product)
        .where(Product.id.in_(product_ids))
    )

    products = result.scalars().all()

    product_map = {p.id: p for p in products}

    ordered_products = [
        product_map[pid]
        for pid in product_ids
        if pid in product_map
    ]

    return ordered_products

async def search_by_image(
    image,
    db: AsyncSession,
    index_path=INDEX_PATH
):
    img_embedding = image_to_embedding(image)
    return await search_products(
        img_embedding,
        db,
        index_path
    )


async def search_by_text(
    text,
    db: AsyncSession,
    index_path=INDEX_PATH
):
    text_embedding = text_to_embedding(text)
    return await search_products(
        text_embedding,
        db,
        index_path
    )
