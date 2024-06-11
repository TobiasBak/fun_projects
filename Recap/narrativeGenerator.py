import torch
from CLIP import clip
from PIL import Image

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load and preprocess the image
image = Image.open("out/images/1.0.0.jpg")
image_input = preprocess(image).unsqueeze(0).to(device)

# Prepare a set of candidate descriptions
descriptions = [
    "a photo of a beautiful landscape",
    "a picture of a busy city street",
    "a photo of a group of people at a party",
    "a picture of a cat",
    "a photo of a dog",
    "a picture of a sunset over the mountains",
    "a photo of the ocean",
    "a picture of a forest",
    "a photo of a car",
    "a picture of a house"
]

# Encode the descriptions and the image
text_inputs = torch.cat([clip.tokenize(desc) for desc in descriptions]).to(device)
with torch.no_grad():
    image_features = model.encode_image(image_input)
    text_features = model.encode_text(text_inputs)

# Calculate similarity
similarities = (image_features @ text_features.T).squeeze(0)
best_match = similarities.argmax().item()
description = descriptions[best_match]

print(f"Best description: {description}")
