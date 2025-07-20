import os

PROJECT_ROOT_PATH = os.path.abspath(os.getenv("PROJECT_ROOT_PATH", ".")).replace("\\","/")
ASSETS_PATH = os.getenv("ASSETS_PATH", os.path.join(PROJECT_ROOT_PATH, "assets")).replace("\\","/")
IMAGE_PATH = os.getenv("IMAGE_PATH", os.path.join(PROJECT_ROOT_PATH, "images")).replace("\\","/")
BIG_BASKET_URL = "https://www.bigbasket.com/product/all-categories/"
LABEL_MAP_PATH = os.path.join(ASSETS_PATH, "label_map_category.json").replace("\\","/")

TRANSFORM = {
    "image": {
        "train_val": {
            "resize": (224, 224),
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225]
        }
    }
}
