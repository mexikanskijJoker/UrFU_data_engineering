import requests
import json
from bs4 import BeautifulSoup


def handle_link(link: str) -> dict():
    response = requests.get(url)
    data = response.text
    product = BeautifulSoup(data, "html.parser")
    result = {}
    result["title"] = product.h2.get_text().strip()
    result["image"] = product.img["data-src"]
    result["link"] = product.find("div", attrs={"class": "product-image"}).a["href"]
    description = (
        product.find("div", attrs={"class": "description"})
        .p.get_text()
        .split(" Грамм Состав: ")
    )
    info, ingredients = (
        product.find("div", attrs={"class": "description"})
        .p.get_text()
        .split("Состав: ")
    )
    result["ingredients"] = list(
        map(str.strip, ingredients.replace(".", "").split(","))
    )
    result["weight"] = int(info.split("Грамм")[0])
    result["size"] = int(info.split("Грамм")[1].replace("см", ""))
    result["price"] = int(
        product.find("span", attrs={"class": "price"}).get_text().replace("руб.", "")
    )
    return result


links = [
    "https://sushkilove.ru/product/zhulen/",
    "https://sushkilove.ru/product/karbonara/",
    "https://sushkilove.ru/product/losos-s-syrom/",
    "https://sushkilove.ru/product/mazhor/",
    "https://sushkilove.ru/product/margarita/",
    "https://sushkilove.ru/product/men-love/",
    "https://sushkilove.ru/product/okean-love/",
    "https://sushkilove.ru/product/ohotnichya/",
    "https://sushkilove.ru/product/pepperoni/",
    "https://sushkilove.ru/product/piczcza-hot-dog/",
    "https://sushkilove.ru/product/s-bekonom-i-gribami/",
    "https://sushkilove.ru/product/halapenyu/",
]

product_data = list()
for url in links:
    product_data.append(handle_link(url))

product_data = sorted(product_data, key=lambda x: x["weight"])
with open("pages_result.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(product_data, ensure_ascii=False))

filtered_data = list(filter(lambda x: len(x["ingredients"]) > 4, product_data))
with open("pages_result_filtered.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_data, ensure_ascii=False))

prices = list(map(lambda x: x["price"], product_data))
prices_stat = {
    "prices_sum": sum(prices),
    "prices_max": max(prices),
    "prices_min": min(prices),
    "prices_average": round(sum(prices) / len(prices), 2),
}
with open("pages_price_statistic.json", "w", encoding="utf-8") as f:
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
with open("pages_ingredients_frequency.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(freq, ensure_ascii=False))
