!pip install torch torchvision

!pip install git+https://github.com/openai/CLIP.git

import torch
import clip
import os
import random
import pandas as pd
from PIL import Image
from IPython.display import display
from google.colab import files

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

csv_path = "/content/vsdatasets.csv"
df = pd.read_csv(csv_path)
labels = df['Label'].tolist()

print("Please upload images (JPG, JPEG, PNG, WEBP, GIF, BMP) for classification...")
uploaded_files = files.upload()

supported_formats = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")
image_files = [file for file in uploaded_files.keys() if file.lower().endswith(supported_formats)]

if not image_files:
    raise ValueError("No valid image files were uploaded. Please upload at least one.")

random_image_path = random.choice(image_files)
print(f"\nSelected Random Image: {random_image_path}")
image = Image.open(random_image_path).convert("RGB")
image_processed = preprocess(image).unsqueeze(0).to(device)

print(f"\nDisplaying Selected Image: {random_image_path}")
display(image)

text_inputs = clip.tokenize(labels).to(device)

with torch.no_grad():
    image_features = model.encode_image(image_processed)
    text_features = model.encode_text(text_inputs)
    similarity = torch.matmul(image_features, text_features.T).squeeze(0)

best_match_idx = similarity.argmax().item()
best_match = labels[best_match_idx]
print(f"\nPredicted Label: {best_match}")

print("\nSimilarity Scores:")
for label, score in zip(labels, similarity.tolist()):
    print(f"{label}: {score:.4f}")
