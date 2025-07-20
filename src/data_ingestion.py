import os
import json
import re
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.ingest.category_scraper import fetch_category_pages
from src.ingest.product_scraper import process_category
from src.ingest.image_downloader import download_image_and_metadata
from src.config import ASSETS_PATH, IMAGE_PATH

def ingest_data():
    categories = fetch_category_pages()

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(process_category, cat) for cat in categories]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Scraping"):
            pass

    args_list = []
    for cat in categories:
        try:
            cat_name = re.sub(r"[^a-zA-Z0-9]", "", cat["category"])
            sub1 = re.sub(r"[^a-zA-Z0-9]", "", cat["sub_category_1"])
            sub2 = re.sub(r"[^a-zA-Z0-9]", "", cat["sub_category_2"])
            file_path = f"{ASSETS_PATH}/product_links/{cat_name}/{sub1}_{sub2}.json"
            with open(file_path) as f:
                products = json.load(f)
            for product in products:
                args_list.append((cat, product, cat))
        except Exception as e:
            print(f"Could not process: {e}")

    metadata = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for result in tqdm(executor.map(download_image_and_metadata, args_list), total=len(args_list), desc="Downloading"):
            if result:
                metadata.append(result)

    df = pd.DataFrame(metadata)
    df.to_csv(f"{IMAGE_PATH}/training_metadata.csv", index=False)
