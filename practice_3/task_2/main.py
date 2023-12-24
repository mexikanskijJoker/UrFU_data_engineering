import json
import re
from bs4 import BeautifulSoup as bs


class Parser:
    def __init__(self) -> None:
        self.path = "data/{}.html"

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
            "name": self._get_name(elem),
            "price": self._get_price(elem),
            "bonuses": self._get_bonuses(elem),
        }
        if self._get_processor(elem) != None:
            res.update({"processor": self._get_processor(elem)})
        if self._get_ram(elem) != None:
            res.update({"ram": self._get_ram(elem)})
        if self._get_sim(elem) != None:
            res.update({"sim": self._get_sim(elem)})
        if self._get_matrix(elem) != None:
            res.update({"matrix": self._get_matrix(elem)})
        if self._get_resolution(elem) != None:
            res.update({"resolution": self._get_resolution(elem)})
        if self._get_acc(elem) != None:
            res.update({"acc": self._get_acc(elem)})

        return res

    def _get_files_data(self):
        data = []

        for i in range(1, 96):
            file = self.path.format(i)
            page = self._get_html(file)
            elems = page.findAll("div", class_="product-item")
            for elem in elems:
                data.append(self._get_data(elem))

        return data

    def _sort_values(self, data):
        return sorted(data, key=lambda obj: obj["price"])

    def _filter_values(self, data):
        return list(filter(lambda obj: obj["bonuses"] > 2000, data))

    def _get_stats(self, data):
        price_stats = [obj["price"] for obj in data]
        return {
            "max": max(price_stats),
            "min": min(price_stats),
            "sum": sum(price_stats),
            "avg": sum(price_stats) / len(price_stats),
        }

    def _get_freq(self, data):
        matrixes = list(map(lambda obj: obj.get("matrix"), data))
        freq = {}
        for matrix in matrixes:
            if matrix in freq:
                freq[matrix] += 1
            else:
                freq[matrix] = 1
        return freq

    def _get_html(self, file):
        with open(file, encoding="UTF-8") as file:
            file_data = file.read()

        return bs(file_data, "html.parser")

    def _get_name(self, elem: bs):
        return elem.find("span").text.strip()

    def _get_price(self, elem):
        price = int(re.sub(r"[\s₽]", "", elem.find("price").text.strip()))
        return price

    def _get_bonuses(self, elem):
        bonuses = int(re.search(r"\d+", elem.find("strong").text.strip()).group(0))
        return bonuses

    def _get_processor(self, elem):
        try:
            processor = elem.find("li", type="processor")
            return processor.text.strip()
        except AttributeError:
            return None

    def _get_ram(self, elem):
        try:
            ram = elem.find("li", type="ram")
            return int(ram.text.strip().replace(" GB", ""))
        except AttributeError:
            return None

    def _get_sim(self, elem):
        try:
            sim = elem.find("li", type="sim")
            return int(sim.text.strip().replace(" SIM", ""))
        except AttributeError:
            return None

    def _get_matrix(self, elem):
        try:
            matrix = elem.find("li", type="matrix")
            return matrix.text.strip()
        except AttributeError:
            return None

    def _get_resolution(self, elem):
        try:
            resolution = elem.find("li", type="resolution")
            return resolution.text.strip()
        except AttributeError:
            return None

    def _get_acc(self, elem):
        try:
            acc = elem.find("li", type="acc")
            return int(acc.text.strip().replace(" мА * ч", ""))
        except AttributeError:
            return None


def main():
    parser = Parser()
    parser.save_data()


if __name__ == "__main__":
    main()
