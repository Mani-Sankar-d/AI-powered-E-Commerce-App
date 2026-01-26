import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, logging
import open_clip
import faiss
import requests
from PIL import Image
from io import BytesIO
import os




# -------------------- CONFIG --------------------

logging.set_verbosity_error()

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DTYPE = torch.float16 if DEVICE.type == "cuda" else torch.float32

BLIP_MODEL_PATH = os.getenv(
    "BLIP_MODEL_PATH",
    "D:/repos/finetuned_models/fine_tuned_blip_fashion"
)

# -------------------- FAISS --------------------

EMBED_DIM = 512
_base_index = faiss.IndexFlatL2(EMBED_DIM)
faiss_index = faiss.IndexIDMap(_base_index)

# -------------------- MODELS (LOAD ONCE) --------------------

print(f"[ML] Loading models on {DEVICE}")

blip_processor = BlipProcessor.from_pretrained(BLIP_MODEL_PATH)
blip_model = BlipForConditionalGeneration.from_pretrained(
    BLIP_MODEL_PATH,
    torch_dtype=DTYPE,
    use_safetensors=True
).to(DEVICE)
blip_model.eval()

clip_model, _, clip_preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai"
)
clip_model = clip_model.to(DEVICE)
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

    img_tensor = clip_preprocess(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        feat = clip_model.encode_image(img_tensor)
        feat = feat / feat.norm(dim=-1, keepdim=True)

    vector = feat.cpu().numpy().astype("float32")

    # Add to FAISS
    faiss_index.add_with_ids(vector, torch.tensor([item_id]))

    return {
        "item_id": item_id,
        "embedding_dim": vector.shape[-1],
    }


def search_similar(vector: torch.Tensor, k: int = 5):
    vec = vector.cpu().numpy().astype("float32")
    distances, ids = faiss_index.search(vec, k)
    return ids[0].tolist(), distances[0].tolist()
