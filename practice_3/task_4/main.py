import json
from bs4 import BeautifulSoup as bs


class Parser:
    def __init__(self) -> None:
        self.path = "data/{}.xml"

    def save_data(self):
        data = self._get_files_data()
        with open("sorted.json", "w", encoding="UTF-8") as file:
            json.dump(self._sort_values(data), file, indent=2, ensure_ascii=False)
        with open("filtered.json", "w", encoding="UTF-8") as file:
            json.dump(self._filter_values(data), file, indent=2, ensure_ascii=False)
        with open("stats.json", "w", encoding="UTF-8") as file:
            json.dump(self._get_stats(data), file, indent=2, ensure_ascii=False)
        with open("freq.json", "w", encoding="UTF-8") as file:
            json.dump(self._get_freq(data), file, indent=2, ensure_ascii=False)

    def _get_data(self, elem: bs):
        return {
            "id": self._get_id(elem),
            "name": self._get_name(elem),
            "category": self._get_category(elem),
            "size": self._get_size(elem),
            "color": self._get_color(elem),
            "material": self._get_material(elem),
            "price": self._get_price(elem),
            "rating": self._get_rating(elem),
            "reviews": self._get_reviews(elem),
            "new": self._get_newness(elem),
            "exclusive": self._get_exclusivity(elem),
            "sporty": self._get_sportiness(elem),
        }

    def _get_files_data(self):
        data = []

        for i in range(1, 101):
            file = self.path.format(i)
            page = self._get_html(file)
            elems = page.findAll("clothing")
            for elem in elems:
                data.append(self._get_data(elem))

        return data

    def _sort_values(self, data):
        return sorted(data, key=lambda obj: obj["price"])

    def _filter_values(self, data):
        return list(filter(lambda obj: obj["reviews"] > 990000, data))

    def _get_stats(self, data):
        ratings = [obj["rating"] for obj in data]
        return {
            "max": max(ratings),
            "min": min(ratings),
            "sum": sum(ratings),
            "avg": sum(ratings) / len(ratings),
        }

    def _get_freq(self, data):
        materials = list(map(lambda obj: obj["material"], data))
        freq = {}
        for material in materials:
            if material in freq:
                freq[material] += 1
            else:
                freq[material] = 1
        return freq

    def _get_html(self, file):
        with open(file, encoding="UTF-8") as file:
            file_data = file.read()

        return bs(file_data, features="xml")

    def _get_id(self, elem: bs):
        return int(elem.find("id").text.strip())

    def _get_name(self, elem: bs):
        name = elem.find("name").text.strip()
        return name

    def _get_category(self, elem: bs):
        category = elem.find("category").text.strip()
        return category

    def _get_size(self, elem: bs):
        size = elem.find("size")
        if size == None:
            return "No data"
        return size.text.strip()

    def _get_color(self, elem: bs):
        color = elem.find("color")
        if color == None:
            return "No data"
        return color.text.strip()

    def _get_material(self, elem):
        material = elem.find("material")
        if material == None:
            return "No data"
        return material.text.strip()

    def _get_price(self, elem):
        price = elem.find("price")
        if price == None:
            return "No data"
        return int(price.text.strip())

    def _get_rating(self, elem):
        rating = elem.find("rating")
        if rating == None:
            return "No data"
        return float(rating.text.strip())

    def _get_reviews(self, elem):
        reviews = elem.find("reviews")
        if reviews == None:
            return "No data"
        return int(reviews.text.strip())

    def _get_newness(self, elem):
        new = elem.find("new")
        if new == None:
            return "No data"
        return new.text.strip()

    def _get_exclusivity(self, elem):
        exclusive = elem.find("exclusive")
        if exclusive == None:
            return "No data"
        return exclusive.text.strip()

    def _get_sportiness(self, elem):
        sporty = elem.find("sporty")
        if sporty == None:
            return "No data"
        return sporty.text.strip()


def main():
    parser = Parser()
    parser.save_data()


if __name__ == "__main__":
    main()
