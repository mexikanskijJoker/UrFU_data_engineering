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

    def _get_data(self, file):
        page = self._get_html(file)

        return {
            "name": self._get_name(page),
            "constellation": self._get_constellation(page),
            "spectral-class": self._get_spectral_class(page),
            "radius": self._get_radius(page),
            "rotation": self._get_rotation(page),
            "age": self._get_age(page),
            "distance": self._get_distance(page),
            "absolute-magnitude": self._get_absolute_magnitude(page),
        }

    def _get_files_data(self):
        data = []
        for i in range(1, 501):
            file = self.path.format(i)
            data.append(self._get_data(file))

        return data

    def _sort_values(self, data):
        return sorted(data, key=lambda obj: obj["radius"])

    def _filter_values(self, data):
        return list(filter(lambda obj: obj["constellation"] == "Лев", data))

    def _get_stats(self, data):
        radiuses = [obj["radius"] for obj in data]
        return {
            "max": max(radiuses),
            "min": min(radiuses),
            "sum": sum(radiuses),
            "avg": sum(radiuses) / len(radiuses),
        }

    def _get_freq(self, data):
        constellations = list(map(lambda obj: obj["constellation"], data))
        freq = {}
        for constellation in constellations:
            if constellation in freq:
                freq[constellation] += 1
            else:
                freq[constellation] = 1
        return freq

    def _get_html(self, file):
        with open(file, encoding="UTF-8") as file:
            file_data = file.read()

        return bs(file_data, features="xml")

    def _get_name(self, page):
        return page.find("name").text.strip()

    def _get_constellation(self, page):
        return page.find("constellation").text.strip()

    def _get_spectral_class(self, page):
        return page.find("spectral-class").text.strip()

    def _get_radius(self, page):
        return int(page.find("radius").text.strip())

    def _get_rotation(self, page):
        return page.find("rotation").text.strip()

    def _get_age(self, page):
        return float(page.find("age").text.strip().replace(" billion years", ""))

    def _get_distance(self, page):
        return page.find("distance").text.strip()

    def _get_absolute_magnitude(self, page):
        return page.find("absolute-magnitude").text.strip()


def main():
    parser = Parser()
    parser.save_data()


if __name__ == "__main__":
    main()
