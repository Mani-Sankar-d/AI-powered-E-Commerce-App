import torch
import requests
from PIL import Image
import open_clip
device = "cuda"
#clip

model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
model = model.to(device)

def getImageEmbedding(url):
    image = Image.open(requests.get(url, stream=True).raw)
    image = preprocess(image).unsqueeze(0)
    image = image.to(device)

    with torch.no_grad(), torch.cuda.amp.autocast():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.to("cpu")

def getTextEmbedding(prompt):
    text = tokenizer([prompt])
    with torch.no_grad(), torch.cuda.amp.autocast():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features
