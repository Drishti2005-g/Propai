import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import json
import os

def train_model():
    print("\n🚀 TRAINING STARTED...\n")

    data_dir = "./dataset/"
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
    ])

    dataset = ImageFolder(data_dir, transform=transform)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    epochs = 5

    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss:.4f}")

    os.makedirs("./models", exist_ok=True)
    torch.save(model.state_dict(), "./models/property_model.pth")

    with open("./models/classes.json", "w") as f:
        json.dump(dataset.classes, f)

    print("\n🎉 MODEL TRAINED AND SAVED SUCCESSFULLY!")
    print("Saved to: models/property_model.pth")
    print("Classes:", dataset.classes)

if __name__ == "__main__":
    train_model()