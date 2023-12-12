import csv
from pymongo import MongoClient
from bson.json_util import dumps


class Jobs:
    def __init__(self, file):
        self.file = file

    def save_data(self):
        collection = self._connect()
        with open("salary_sort.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(self._get_sorted_docs(collection), indent=2, ensure_ascii=False)
            )
        with open("age_filter.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_filtered_data_by_age(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("my_condition.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_filtered_data_by_random_condition(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("year_and_salary_filter.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_filtered_data_by_year_and_salary(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )

    def set_db_data(self):
        collection = self._connect()
        collection.insert_many(self._get_file_data())

    def _connect(self):
        client = MongoClient()
        db = client["practice_5"]

        return db.jobs

    def _get_file_data(self):
        data = []
        with open(self.file, encoding="UTF-8") as file:
            reader = csv.reader(file, delimiter=";")
            rows = [row for row in reader]
        for row in rows[1:]:
            data.append(
                {
                    "job": row[0],
                    "salary": int(row[1]),
                    "id": int(row[2]),
                    "city": row[3],
                    "year": int(row[4]),
                    "age": int(row[5]),
                }
            )

        return data

    def _get_filtered_data_by_age(self, collection):
        data = collection.find({"age": {"$lt": 30}}, limit=15).sort({"salary": -1})

        return list(data)

    def _get_filtered_data_by_random_condition(self, collection):
        data = collection.find(
            {
                "city": "Варшава",
                "job": {"$in": ["Менеджер", "Косметолог", "Медсестра"]},
            },
            limit=10,
        ).sort({"age": 1})

        return list(data)

    def _get_filtered_data_by_year_and_salary(self, collection):
        data = collection.find(
            {
                "age": {"$gt": 17, "$lt": 25},
                "year": {"$in": [2019, 2020, 2021, 2022]},
                "$or": [
                    {"salary": {"$gt": 50000, "$lte": 75000}},
                    {"salary": {"$gt": 125000, "$lte": 150000}},
                ],
            }
        )

        return list(data)

    def _get_sorted_docs(self, collection):
        data = collection.find({}, limit=10).sort({"salary": -1})

        return list(data)


def main():
    jobs = Jobs("task_1_item.csv")
    jobs.set_db_data()
    jobs.save_data()


if __name__ == "__main__":
    main()
