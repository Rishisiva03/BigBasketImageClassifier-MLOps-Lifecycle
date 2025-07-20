import os
import json
import re
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from src.config import ASSETS_PATH

def scrape_webpage(webpage_url: str) -> BeautifulSoup:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(webpage_url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
    )
    html = driver.page_source
    driver.quit()
    return BeautifulSoup(html, "html.parser")

def parse_soup(soup):
    products_list = []
    products_soup = soup.find("section", class_="z-10")
    for product_soup in products_soup.find_all("li"):
        image_src = product_soup.find("img").get("src") if product_soup.find("img") else None
        if image_src:
            products_list.append({
                "name": getattr(product_soup.find("div", class_="break-words h-10 w-full"), "text", None),
                "sku_type": getattr(product_soup.find("span", class_="Label-sc-15v1nk5-0 gJxZPQ truncate"), "text", None),
                "rating": getattr(product_soup.find("span", class_="Label-sc-15v1nk5-0 gJxZPQ"), "text", None),
                "image_link": image_src,
            })
    return products_list

def process_category(category: dict):
    try:
        category_name = re.sub(r"[^a-zA-Z0-9]", "", category["category"])
        sub1 = re.sub(r"[^a-zA-Z0-9]", "", category["sub_category_1"])
        sub2 = re.sub(r"[^a-zA-Z0-9]", "", category["sub_category_2"])
        link = category["link"]

        dir_name = f"{ASSETS_PATH}/product_links/{category_name}/"
        os.makedirs(dir_name, exist_ok=True)
        file_name = f"{dir_name}{sub1}_{sub2}.json"

        products_list = parse_soup(scrape_webpage(link))

        try:
            with open(file_name, "r") as f:
                old = json.load(f)
                links = {item["image_link"] for item in old}
                products_list += [item for item in old if item["image_link"] not in links]
        except:
            pass

        with open(file_name, "w") as f:
            json.dump(products_list, f, indent=2)

        return file_name
    except Exception:
        traceback.print_exc()
        return None
