import faiss
import numpy as np
from sqlalchemy import select
from backend.db import AsyncSessionLocal
from backend.models.product import Product

FAISS_PATH = "D:/repos/AI-powered-E-commerce/backend/ml_service/workers/products.faiss"


async def main():
    index = faiss.read_index(FAISS_PATH)

    print("Total vectors:", index.ntotal)

    # Get all IDs from IndexIDMap
    ids = faiss.vector_to_array(index.id_map)

    print("First 10 FAISS IDs:")
    print(ids[:10])

    async with AsyncSessionLocal() as db:
        for pid in ids[:10]:
            product = await db.get(Product, int(pid))

            if product is None:
                print(f"❌ Product {pid} not found in DB")
            else:
                print(
                    f"✅ id={product.id} "
                    f"name={product.name} "
                    f"indexed={product.indexed}"
                )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())