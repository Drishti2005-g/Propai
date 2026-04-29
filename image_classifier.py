import torch
from torchvision import models, transforms
from PIL import Image
import json
import os

MODEL_PATH = "./models/property_model.pth"
CLASSES_PATH = "./models/classes.json"

# Load model + classes
def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(CLASSES_PATH):
        print("⚠ Model not found! Please train the image classifier first.")
        return None, None

    # Load class names
    with open(CLASSES_PATH, "r") as f:
        classes = json.load(f)

    # Create the model architecture
    model = models.resnet18()
    model.fc = torch.nn.Linear(model.fc.in_features, len(classes))

    # Load weights
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
    model.eval()

    return model, classes


# Transform image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# Predict function
def classify_property(img_path):
    model, classes = load_model()

    # If model not found
    if model is None:
        return "Model not trained"

    img = Image.open(img_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)  # batch of 1

    with torch.no_grad():
        output = model(tensor)
        _, prediction = torch.max(output, 1)

    return classes[prediction.item()]