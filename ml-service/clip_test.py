import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests
from PIL import Image
from io import BytesIO
from transformers import logging
import open_clip
import faiss
device = "cuda"
#clip
clip_model, _, clip_preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
clip_tokenizer = open_clip.get_tokenizer('ViT-B-32')
clip_model = clip_model.to(device)

