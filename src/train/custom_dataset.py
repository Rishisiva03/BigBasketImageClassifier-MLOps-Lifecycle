from torch.utils.data import Dataset
from PIL import Image

class GroceryDataset(Dataset):
    def __init__(self, df, transform):
        self.df = df.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        image = Image.open(row["filename"]).convert("RGB")
        image = self.transform(image)
        label = row["label"]
        return image, label
