
import pandas as pd
import torch
from torch.utils.data import DataLoader

from src.config import IMAGE_PATH
from src.train.custom_dataset import GroceryDataset
from src.train.label_encoder import encode_labels, split_dataset
from src.train.model import get_model
from src.train.model import train_model, evaluate_model, get_transform

def train():
    metadata_df = pd.read_csv(f"{IMAGE_PATH}/training_metadata.csv")
    metadata_df, label_map = encode_labels(metadata_df)
    train_df, val_df = split_dataset(metadata_df)

    transform = get_transform()
    train_ds = GroceryDataset(train_df, transform)
    val_ds = GroceryDataset(val_df, transform)
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model(num_classes=metadata_df["label"].nunique())

    model = train_model(model, train_loader, device, epochs=15)
    evaluate_model(model, val_loader, device, label_map)

