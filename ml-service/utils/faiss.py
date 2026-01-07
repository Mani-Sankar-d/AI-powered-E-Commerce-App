import faiss
import numpy as np

FAISS_PATH = "products.faiss"

def addEmbedding(index, embedding):
    faiss.write_index(index, FAISS_PATH)
    embedding = np.array(embedding, dtype="float32").reshape(1,-1)
    faiss.normalize_L2(embedding)
    faiss_id = index.ntotal
    index.add(embedding)
    return faiss_id

def search(index, query):
    faiss.normalize_L2(query)
    k=5
    distances, ids = index.search(query, k)
    return ids