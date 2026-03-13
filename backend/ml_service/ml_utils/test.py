from backend.ml_service.ml_utils.model import search_by_text
from PIL import  Image
import pickle
I,_ = search_by_text("denim jeans jacket")
with open("paths.pkl","rb") as f:
    paths = pickle.load(f)
root = "D:/repos/Recommendation"
def display(I, paths):
    for idx in I:
        Image.open(root+paths[idx][1:]).show()

display(I,paths)
