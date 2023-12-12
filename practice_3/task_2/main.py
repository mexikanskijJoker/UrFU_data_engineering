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
        return {
            "name": self._get_name(elem),
            "price": self._get_price(elem),
            "bonuses": self._get_bonuses(elem),
            "processor": self._get_processor(elem),
            "ram": self._get_ram(elem),
            "sim": self._get_sim(elem),
            "matrix": self._get_matrix(elem),
            "resolution": self._get_resolution(elem),
            "acc": self._get_acc(elem),
        }

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
        return list(filter(lambda obj: obj["ram"] == "No data", data))

    def _get_stats(self, data):
        acc_capacity = [obj["acc"] for obj in data if obj["acc"] != "No data"]
        return {
            "max": max(acc_capacity),
            "min": min(acc_capacity),
            "sum": sum(acc_capacity),
            "avg": sum(acc_capacity) / len(acc_capacity),
        }

    def _get_freq(self, data):
        matrixes = list(map(lambda obj: obj["matrix"], data))
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
        processor = elem.find("li", type="processor")
        if processor == None:
            return "No data"
        return processor.text.strip()

    def _get_ram(self, elem):
        ram = elem.find("li", type="ram")
        if ram == None:
            return "No data"
        return int(ram.text.strip().replace(" GB", ""))

    def _get_sim(self, elem):
        sim = elem.find("li", type="sim")
        if sim == None:
            return "No data"
        return int(sim.text.strip().replace(" SIM", ""))

    def _get_matrix(self, elem):
        matrix = elem.find("li", type="matrix")
        if matrix == None:
            return "No data"
        return matrix.text.strip()

    def _get_resolution(self, elem):
        resolution = elem.find("li", type="resolution")
        if resolution == None:
            return "No data"
        return resolution.text.strip()

    def _get_acc(self, elem):
        acc = elem.find("li", type="acc")
        if acc == None:
            return "No data"
        return int(acc.text.strip().replace(" мА * ч", ""))


def main():
    parser = Parser()
    parser.save_data()


if __name__ == "__main__":
    main()
