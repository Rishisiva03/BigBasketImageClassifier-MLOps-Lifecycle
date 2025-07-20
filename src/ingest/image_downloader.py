import os
import requests
import pandas as pd
from src.config import IMAGE_PATH
from src.utils import sanitize_filename

try:
    metadata_df = pd.read_csv(f"{IMAGE_PATH}/training_metadata.csv")
except:
    metadata_df = None

def download_image_and_metadata(args):
    category, product, meta = args
    image_link = product.get("image_link")
    if not image_link:
        return None

    name = product.get("name")
    ext = image_link.split(".")[-1].split("?")[0]
    filename = f"{sanitize_filename(name)}.{ext}"
    dirpath = os.path.join(IMAGE_PATH, sanitize_filename(meta["category"]))
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, filename)

    if metadata_df is not None and not metadata_df[metadata_df["image_link"] == image_link].empty:
        return None

    try:
        if not os.path.exists(filepath):
            response = requests.get(image_link, timeout=10)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)

        return {
            **meta,
            "filename": os.path.abspath(filepath),
            "name": name,
            "sku_type": product.get("sku_type"),
            "rating": product.get("rating"),
            "image_link": image_link,
        }

    except Exception as e:
        print(f"Error downloading {image_link}: {e}")
        return None
