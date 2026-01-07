from fastapi import FastAPI
from model import generate_caption
from utils.embedding_generator import getImageEmbedding
from utils.faiss import addEmbedding
import faiss
import os
FAISS_PATH = "products.faiss"
D=512

app = FastAPI()


@app.on_event("startup")
async def load_faiss():
    global index
    if os.path.exists(FAISS_PATH):
        index = faiss.read_index(FAISS_PATH)
        print("Loaded faiss from disk")
    else:
        index = faiss.IndexFlatIP(D)
        print("Created new faiss index")

@app.post("/caption")
def caption(payload:dict):
    # print("Reached endpoint")
    return generate_caption(payload)

@app.post("/enterEmbedding")
async def computeEmbedding(payload:dict):
    global index
    url = payload["url"]
    embedding = getImageEmbedding(url)
    faissId = addEmbedding(index, embedding)
    return {"faissId":faissId}