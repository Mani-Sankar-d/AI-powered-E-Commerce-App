import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, logging
import faiss
import requests
from PIL import Image
from io import BytesIO
import os
import numpy as np
import pickle


logging.set_verbosity_error()
# with open("paths.pkl","rb") as f:
#     paths = pickle.load(f)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DTYPE = torch.float16 if DEVICE.type == "cuda" else torch.float32

BLIP_MODEL_PATH = os.getenv("BLIP_MODEL_PATH")


print(f"[ML] Loading models on {DEVICE}")

blip_processor = BlipProcessor.from_pretrained(BLIP_MODEL_PATH)
blip_model = BlipForConditionalGeneration.from_pretrained(
    BLIP_MODEL_PATH,
    torch_dtype=DTYPE,
    use_safetensors=True
).to(DEVICE)
blip_model.eval()



def _load_image(url: str) -> Image.Image:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img


def generate_caption(payload: dict) -> dict:
    if "image" not in payload:
        raise ValueError("Missing required field: image")

    img = _load_image(payload["image"])
    user_text = payload.get("description")

    inputs = blip_processor(
        images=img,
        text=user_text,
        return_tensors="pt"
    ).to(DEVICE, DTYPE)
    
    with torch.no_grad():
        output = blip_model.generate(**inputs)

    caption = blip_processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return {"caption": caption}