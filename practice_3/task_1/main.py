from pprint import pprint
from bs4 import BeautifulSoup as bs
import json
import re


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

    def _get_data(self, file):
        page = self._get_html(file)

        return {
            "town": self._get_town(page),
            "title": self._get_title(page),
            "address": self._get_address(page),
            "floors": self._get_floors(page),
            "year": self._get_year(page),
            "rating": self._get_rating(page),
            "views": self._get_views(page),
        }

    def _get_files_data(self):
        data = []
        for i in range(1, 1000):
            file = self.path.format(i)
            data.append(self._get_data(file))

        return data

    def _sort_values(self, data):
        return sorted(data, key=lambda obj: obj["rating"])

    def _filter_values(self, data):
        return list(filter(lambda obj: obj["views"] > 95000, data))

    def _get_stats(self, data):
        ratings = [obj["rating"] for obj in data]
        return {
            "max": max(ratings),
            "min": min(ratings),
            "sum": sum(ratings),
            "avg": sum(ratings) / len(ratings),
        }

    def _get_freq(self, data):
        towns = list(map(lambda obj: obj["town"], data))
        freq = {}
        for town in towns:
            if town in freq:
                freq[town] += 1
            else:
                freq[town] = 1
        return freq

    def _get_html(self, file):
        with open(file, encoding="UTF-8") as file:
            file_data = file.read()

        return bs(file_data, "html.parser")

    def _get_town(self, page):
        return page.find("span").text.split(":")[1].strip()

    def _get_title(self, page):
        return (
            page.find("h1", class_="title").text.replace("\n", "").split(":")[1].strip()
        )

    def _get_address(self, page):
        return (
            page.find("p", class_="address-p")
            .text.replace("\n", "")
            .split(":", maxsplit=1)[1]
            .strip()
        )

    def _get_floors(self, page):
        return int(page.find("span", class_="floors").text.split(":")[1].strip())

    def _get_year(self, page):
        return int(
            re.search(r"\d+", page.find("span", class_="year").text.strip()).group(0)
        )

    def _get_rating(self, page):
        return float(page.findAll("span")[4].text.split(":")[1].strip())

    def _get_views(self, page):
        return int(page.findAll("span")[5].text.split(":")[1].strip())


def main():
    parser = Parser()
    parser.save_data()
    # pprint(parser.sort_values())

    # with open("sorted.json", "w", encoding="UTF-8") as file:
    #     json.dump(
    #         sorted(data, key=lambda x: x["rating"]), file, indent=2, ensure_ascii=False
    #     )


if __name__ == "__main__":
    main()
