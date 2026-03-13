import warnings
warnings.filterwarnings("ignore")
import torch
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import numpy as np
import pickle
import faiss
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

model.eval()
def image_to_embedding(path):
    img = Image.open(path).convert("RGB")
    inputs = processor(
        images=img,
        return_tensors="pt"
    ).to(device)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    embedding = embedding.cpu().numpy()[0]
    return embedding

def text_to_embedding(text):
    print("text embedding generation initiating")
    inputs = processor(
        text=[text],return_tensors='pt',padding=True,truncation=True
    ).to(device)
    with torch.no_grad():
        embedding = model.get_text_features(**inputs)
    print("text embedding generation completed")
    embedding = embedding.cpu().numpy()[0]
    return embedding

# def display(I, paths):
#     for idx in I[0]:
#         Image.open(paths[idx]).show()
def search(query_vec,index_path):
    query_vec = query_vec / np.linalg.norm(query_vec)
    with open("paths.pkl", "rb") as f:
        paths = pickle.load(f)
    index = faiss.read_index(index_path)
    D,I = index.search(query_vec.reshape(1,-1),15)
    result_paths = [paths[i] for i in I[0]]
    return I,result_paths
def search_by_image(image_path,index_path="fashion.index"):
    img_embedding = image_to_embedding(image_path)
    return search(img_embedding,index_path)

def search_by_text(text,index_path="fashion.index"):
    text_embedding = text_to_embedding(text)
    I,paths = search(text_embedding,index_path)
    image_urls = [f"/images{p[1:]}" for p in paths]
    print(image_urls[0])
    return image_urls