import requests
import json
from bs4 import BeautifulSoup

url = "https://sushkilove.ru/product-category/zakazt-rolly-verhniy-ufaley/"
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, "html.parser")

products = soup.find_all("div", attrs={"class": "product-inner"})

product_data = list()
for product in products:
    item = {}
    item["title"] = product.h3.get_text()
    item["image"] = product.img["data-src"]
    item["link"] = product.find("div", attrs={"class": "product-image"}).a["href"]
    description = (
        product.find("div", attrs={"class": "description"})
        .p.get_text()
        .split(" Грамм Состав: ")
    )
    item["weight"] = int(description[0])
    item["ingredients"] = description[1].replace(".", "").split(", ")
    item["price"] = int(
        product.find("span", attrs={"class": "price"}).get_text().replace("руб.", "")
    )
    product_data.append(item)

product_data = sorted(product_data, key=lambda x: x["weight"])
with open("catalog_result.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(product_data, ensure_ascii=False))

filtered_data = list(filter(lambda x: len(x["ingredients"]) > 2, product_data))
with open("catalog_result_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_data, ensure_ascii=False))

prices = list(map(lambda x: x["price"], product_data))
prices_stat = {
    "prices_sum": sum(prices),
    "prices_max": max(prices),
    "prices_min": min(prices),
    "prices_average": round(sum(prices) / len(prices), 2),
}
with open("price_statistic.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(prices_stat))

ingredients = list()
for lst in list(map(lambda x: x["ingredients"], product_data)):
    ingredients += lst
freq = {}
for item in ingredients:
    name = item.lower()
    if name in freq:
        freq[name] += 1
    else:
        freq[name] = 1
with open("ingredients_frequency.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(freq, ensure_ascii=False))
