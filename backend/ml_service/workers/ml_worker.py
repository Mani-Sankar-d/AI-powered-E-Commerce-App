import asyncio
from pathlib import Path
import faiss,os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import AsyncSessionLocal, engine
from backend.models.product import Product
from backend.ml_service.ml_utils.model import generate_caption
from backend.ml_service.ml_utils.embedding_generator import getImageEmbedding
from backend.ml_service.ml_utils.faiss import add_embedding



BASE_DIR = Path(__file__).resolve().parent
FAISS_PATH = os.getenv("INDEX_PATH")
EMBED_DIM = 512


def load_faiss_index():
    if FAISS_PATH.exists():
        print("Loading FAISS index from disk")
        return faiss.read_index(str(FAISS_PATH))

    print("Creating new FAISS index")
    return faiss.IndexIDMap(faiss.IndexFlatIP(EMBED_DIM))


index = load_faiss_index()

async def process_product(product: Product, db: AsyncSession):
    try:
        caption = generate_caption({
            "image": product.img_url,
            "description": product.user_description
        })
        embedding = getImageEmbedding(product.img_url)

        add_embedding(
            index=index,
            embedding=embedding,
            faiss_id=product.id,
            faiss_path=FAISS_PATH
        )

        product.description = caption["caption"]
        product.faiss_id = product.id
        product.indexed = True
        product.status = "READY"

        await db.commit()
        print(f"Product {product.id} processed")

    except Exception as e:
        await db.rollback()

        product.status = "FAILED"
        product.ml_error = str(e)

        await db.commit()
        print(f"Product {product.id} failed: {e}")



async def worker_loop():
    print("ML Worker started")

    while True:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Product)
                .where(Product.status == "PENDING")
                .with_for_update(skip_locked=True)
                .limit(1)
            )

            product = result.scalar_one_or_none()

            if not product:
                await asyncio.sleep(3)
                continue


            product.status = "PROCESSING"
            await db.commit()

            await process_product(product, db)



if __name__ == "__main__":
    asyncio.run(worker_loop())
