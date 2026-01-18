import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests
from PIL import Image
from io import BytesIO
from transformers import logging
import open_clip

import faiss
import os
# print("CWD:", os.getcwd())
# print("DATABASE_URL:", os.getenv("DATABASE_URL"))

base_index = faiss.IndexFlatL2(512)
index = faiss.IndexIDMap(base_index)


logging.set_verbosity_error()
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32


#blip
blip_processor = BlipProcessor.from_pretrained("D:/repos/finetuned_models/fine_tuned_blip_fashion")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "D:/repos/finetuned_models/fine_tuned_blip_fashion",
    torch_dtype=torch.float16,
    use_safetensors=True
).to(device)


#clip
clip_model, _, clip_preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
clip_tokenizer = open_clip.get_tokenizer('ViT-B-32')
clip_model = clip_model.to(device)


async def generate_caption(payload):
    if "image" not in payload:
        raise ValueError("Missing required field: image")

    image_url = payload["image"]
    user_text = payload.get("description")

    response = requests.get(payload["image"], headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    inputs = blip_processor(images=img,text=user_text, return_tensors="pt").to(device, dtype)
    o = blip_model.generate(**inputs)
    caption = blip_processor.decode(o[0], skip_special_tokens=True)
    return {"caption":caption}


async def generate_embeddings(payload):
    if "image" not in payload:
        raise ValueError("Missing required field: image")
    image_url = payload["image"]
    user_text = payload.get("description")

    response = requests.get(payload["image"], headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    img_tensor = clip_preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = clip_model.encode_image(img_tensor)
        feat = feat / feat.norm(dim=-1, keepdim=True)
    feat_np = (
        feat
        .detach()
        .cpu()
        .numpy()
        .astype("float32")
    )



