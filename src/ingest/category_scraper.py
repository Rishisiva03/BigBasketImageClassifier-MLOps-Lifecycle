import json
import requests
from bs4 import BeautifulSoup
from src.config import BIG_BASKET_URL, ASSETS_PATH

def fetch_category_pages() -> list[dict]:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
    }
    content = requests.get(BIG_BASKET_URL, headers=headers).text
    soup = BeautifulSoup(content, "html.parser")

    categories = []
    for heading, cover in zip(
        soup.find_all("div", class_="dp_headding"),
        soup.find_all("div", class_="uiv2-search-category-listing-cover"),
    ):
        for s in cover:
            subcat1soup = s.find_all("div", class_="uiv2-search-cover")
            for Sub in subcat1soup:
                subCat = Sub.find("span").text
                for subCat2soup in Sub.find_all("li"):
                    subCat2 = subCat2soup.text
                    categories.append({
                        "category": heading.text,
                        "sub_category_1": subCat,
                        "sub_category_2": subCat2,
                        "link": "https://www.bigbasket.com" +
                                subCat2soup.find("a").get("href") + "#!page=1",
                    })

    with open(f"{ASSETS_PATH}/categories.json", "w") as f:
        json.dump(categories, f, indent=2)

    return categories
