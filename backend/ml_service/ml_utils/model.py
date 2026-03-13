import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, logging
import faiss
import requests
from PIL import Image
from io import BytesIO
import os
import numpy as np


# -------------------- CONFIG --------------------

logging.set_verbosity_error()
with open("paths.pkl","rb") as f:
    paths = pickle.load(f)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DTYPE = torch.float16 if DEVICE.type == "cuda" else torch.float32

BLIP_MODEL_PATH = os.getenv(
    "BLIP_MODEL_PATH",
    "D:/repos/finetuned_models/fine_tuned_blip_fashion"
)

# -------------------- FAISS --------------------

EMBED_DIM = 512
faiss_index = faiss.read_index("fashion.index")

# -------------------- MODELS (LOAD ONCE) --------------------

print(f"[ML] Loading models on {DEVICE}")

blip_processor = BlipProcessor.from_pretrained(BLIP_MODEL_PATH)
blip_model = BlipForConditionalGeneration.from_pretrained(
    BLIP_MODEL_PATH,
    torch_dtype=DTYPE,
    use_safetensors=True
).to(DEVICE)
blip_model.eval()
from transformers import CLIPModel, CLIPProcessor

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

clip_model.eval()

# -------------------- HELPERS --------------------

def _load_image(url: str) -> Image.Image:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img

# -------------------- TASKS --------------------

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


def generate_embedding(payload: dict, item_id: int) -> dict:
    if "image" not in payload:
        raise ValueError("Missing required field: image")

    img = _load_image(payload["image"])

    inputs = clip_processor(
        images=img,
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        feat = clip_model.get_image_features(**inputs)

    feat = feat / feat.norm(dim=-1, keepdim=True)

    vector = feat.cpu().numpy().astype("float32")

    # Add to FAISS
    faiss_index.add_with_ids(vector, np.array([item_id]))

    return {
        "item_id": item_id,
        "embedding_dim": vector.shape[-1],
    }
def image_to_embedding(path):
    img = Image.open(path).convert("RGB")
    inputs = clip_processor(
        images=img,
        return_tensors="pt"
    ).to(DEVICE)
    with torch.no_grad():
        embedding = clip_model.get_image_features(**inputs)
    embedding = embedding.cpu().numpy()[0]
    return embedding

def text_to_embedding(text):
    inputs = clip_processor(
        text=[text],return_tensors='pt',padding=True,truncation=True
    ).to(DEVICE)
    with torch.no_grad():
        embedding = clip_model.get_text_features(**inputs)
    embedding = embedding.cpu().numpy()[0]
    return embedding
def search_by_image(image_path):
    img_embedding = image_to_embedding(image_path)
    return search_similar(img_embedding)

def search_by_text(text):
    text_embedding = text_to_embedding(text)
    return search_similar(text_embedding)
def search_similar(vector, k: int = 5):
    vec = vector.astype("float32").reshape(1, -1)
    distances, ids = faiss_index.search(vec, k)
    return ids[0].tolist(), paths
