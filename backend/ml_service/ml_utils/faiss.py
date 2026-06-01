# utils/faiss.py
from pathlib import Path
import faiss
import numpy as np


def load_faiss_index(dimension: int, faiss_path: Path):

    if faiss_path.exists():
        return faiss.read_index(str(faiss_path))

    return faiss.IndexIDMap(faiss.IndexFlatIP(dimension)) # indexflatIP is the inner prodict methos of storage and by defautl
                        # it stores mapping from vector to index like 1,2,3 IndexIDMap wrapper helps us to give separte id for
                        #referencing from db


def add_embedding(index, embedding, faiss_id: int, faiss_path: Path):

    embedding = np.array(embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(embedding)

    index.add_with_ids(
        embedding,
        np.array([faiss_id], dtype="int64") # ids are expected to be np
    )

    faiss.write_index(index, str(faiss_path))
