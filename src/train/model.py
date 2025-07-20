import torch.nn as nn
from torchvision import models
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report
from torchvision import transforms
from src.config import TRANSFORM

def get_model(num_classes):
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def get_transform():
    return transforms.Compose([
        transforms.Resize(TRANSFORM["image"]["train_val"]["resize"]),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=TRANSFORM["image"]["train_val"]["mean"],
            std=TRANSFORM["image"]["train_val"]["std"]
        )
    ])


def train_model(model, train_loader, device, epochs=10, lr=1e-4):
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.long().to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[Epoch {epoch+1}] Loss: {total_loss:.4f}")
    return model

def evaluate_model(model, val_loader, device, label_map):
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            outputs = model(images)
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.numpy())

    print(classification_report(
        all_labels,
        all_preds,
        target_names=list(label_map.keys()),
        labels=list(label_map.values())
    ))
