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
        res = {
            "id": self._get_id(elem),
            "name": self._get_name(elem),
            "category": self._get_category(elem),
        }

        if self._get_size(elem) != None:
            res.update({"size": self._get_size(elem)})
        if self._get_color(elem) != None:
            res.update({"color": self._get_color(elem)})
        if self._get_material(elem) != None:
            res.update({"material": self._get_material(elem)})
        if self._get_price(elem) != None:
            res.update({"price": self._get_price(elem)})
        if self._get_rating(elem) != None:
            res.update({"rating": self._get_rating(elem)})
        if self._get_reviews(elem) != None:
            res.update({"reviews": self._get_reviews(elem)})
        if self._get_newness(elem) != None:
            res.update({"new": self._get_newness(elem)})
        if self._get_exclusivity(elem) != None:
            res.update({"exclusive": self._get_exclusivity(elem)})
        if self._get_sportiness(elem) != None:
            res.update({"sporty": self._get_sportiness(elem)})

        return res

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
        categorys = list(map(lambda obj: obj["category"], data))
        freq = {}
        for category in categorys:
            if category in freq:
                freq[category] += 1
            else:
                freq[category] = 1
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
        try:
            size = elem.find("size").text.strip()
            return size
        except AttributeError:
            return None

    def _get_color(self, elem: bs):
        try:
            color = elem.find("color").text.strip()
            return color
        except AttributeError:
            return None

    def _get_material(self, elem):
        try:
            material = elem.find("material").text.strip()
            return material
        except AttributeError:
            return None

    def _get_price(self, elem):
        try:
            price = elem.find("price").text.strip()
            return int(price)
        except AttributeError:
            return None

    def _get_rating(self, elem):
        try:
            rating = elem.find("rating").text.strip()
            return float(rating)
        except AttributeError:
            return None

    def _get_reviews(self, elem):
        try:
            reviews = elem.find("reviews")
            return int(reviews.text.strip())
        except AttributeError:
            return None

    def _get_newness(self, elem):
        try:
            new = elem.find("new").text.strip()
            return True if new == "+" else False
        except AttributeError:
            return None

    def _get_exclusivity(self, elem):
        try:
            exclusive = elem.find("exclusive").text.strip()
            return True if exclusive == "yes" else False
        except AttributeError:
            return None

    def _get_sportiness(self, elem):
        try:
            sporty = elem.find("sporty").text.strip()
            return True if sporty == "yes" else False
        except AttributeError:
            return None


def main():
    parser = Parser()
    parser.save_data()


if __name__ == "__main__":
    main()
