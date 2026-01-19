# utils/faiss.py
from pathlib import Path
import faiss
import numpy as np


def load_faiss_index(dimension: int, faiss_path: Path):
    """
    Load FAISS index from disk if present, else create a new one.
    """
    if faiss_path.exists():
        return faiss.read_index(str(faiss_path))

    return faiss.IndexIDMap(faiss.IndexFlatIP(dimension))


def add_embedding(index, embedding, faiss_id: int, faiss_path: Path):
    """
    Add an embedding to FAISS using an explicit ID (DB primary key)
    and persist the index to disk.
    """
    embedding = np.array(embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(embedding)

    index.add_with_ids(
        embedding,
        np.array([faiss_id], dtype="int64")
    )

    faiss.write_index(index, str(faiss_path))
