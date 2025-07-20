import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from src.config import LABEL_MAP_PATH

def encode_labels(df: pd.DataFrame):
    df = df.dropna(subset=["filename", "category"])
    df = df[df["filename"].apply(os.path.exists)]

    counts = df["category"].value_counts()
    valid_labels = counts[counts >= 2].index
    df = df[df["category"].isin(valid_labels)].reset_index(drop=True)

    le = LabelEncoder()
    df["label"] = le.fit_transform(df["category"])

    label_map = {label: int(index) for label, index in zip(le.classes_, le.transform(le.classes_))}

    with open(LABEL_MAP_PATH, "w") as f:
        json.dump(label_map, f, indent=2)

    return df, label_map

def split_dataset(df, test_size=0.2, seed=42):
    return train_test_split(df, test_size=test_size, stratify=df["label"], random_state=seed)
