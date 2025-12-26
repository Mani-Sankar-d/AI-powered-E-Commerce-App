from fastapi import FastAPI
from model import generate_caption

app = FastAPI()
@app.post("/caption")
async def caption(payload:dict):
    # print("Reached endpoint")
    return generate_caption(payload)