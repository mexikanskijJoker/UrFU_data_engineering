from pymongo import MongoClient

from bson.json_util import dumps


class Jobs:
    def __init__(self, file):
        self.file = file

    def save_data(self):
        collection = self._connect()
        self._set_db_data()
        with open("salary_stats.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_salary_stats(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("jobs_freq.json", "w", encoding="utf-8") as file:
            file.write(
                dumps(self._get_jobs_freq(collection), indent=2, ensure_ascii=False)
            )
        with open("max_age_min_salary.json", "w", encoding="utf-8") as file:
            file.write(
                dumps(
                    self._get_min_salary_max_age(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("min_age_max_salary.json", "w", encoding="utf-8") as file:
            file.write(
                dumps(
                    self._get_max_salary_min_age(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("filtered_by_town.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_filtered_data_by_town(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("filtered_data_by_town_age_job.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_filtered_data_by_town_age_job(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        with open("random_data.json", "w", encoding="UTF-8") as file:
            file.write(
                dumps(
                    self._get_random_data(collection),
                    indent=2,
                    ensure_ascii=False,
                )
            )

    def _connect(self):
        client = MongoClient()
        db = client["task_2"]

        return db.task_2

    def _get_file_data(self):
        with open(self.file, encoding="UTF-8") as file:
            data = file.read()
        file_data = []
        people = data.split("=====")
        for person in people:
            item = {}
            for row in person.strip().split("\n"):
                if row:
                    k, v = row.split("::")[0], row.split("::")[1]
                    if k in ["job", "city"]:
                        item[k] = v
                    else:
                        item[k] = int(v)
            file_data.append(item)

        return file_data

    def _set_db_data(self):
        collection = self._connect()
        data = self._get_file_data()
        collection.insert_many(data)

    def _get_salary_stats(self, collection):
        stats = [
            {
                "$group": {
                    "_id": "salary info",
                    "min_salary": {"$min": "$salary"},
                    "max_salary": {"$max": "$salary"},
                    "avg_salary": {"$avg": "$salary"},
                }
            }
        ]
        data = collection.aggregate(stats)

        return data

    def _get_jobs_freq(self, collection):
        freq = [
            {"$group": {"_id": "$job", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        data = collection.aggregate(freq)

        return list(data)

    def _get_max_salary_min_age(self, collection):
        query = [{"$sort": {"age": -1, "salary": 1}}, {"$limit": 1}]
        items = []
        for row in collection.aggregate(query):
            row["_id"] = str(row["_id"])
            items.append(row)

        return items

    def _get_min_salary_max_age(self, collection):
        query = [{"$sort": {"age": 1, "salary": -1}}, {"$limit": 1}]
        items = []
        for row in collection.aggregate(query):
            row["_id"] = str(row["_id"])
            items.append(row)

        return items

    def _get_filtered_data_by_town(self, collection):
        stats = [
            {"$match": {"salary": {"$gt": 50000}}},
            {
                "$group": {
                    "_id": "$city",
                    "min_age": {"$min": "$age"},
                    "max_age": {"$max": "$age"},
                    "avg_age": {"$avg": "$age"},
                }
            },
            {"$sort": {"avg_age": -1}},
        ]
        data = collection.aggregate(stats)

        return list(data)

    def _get_filtered_data_by_town_age_job(self, collection):
        stats = [
            {
                "$match": {
                    "city": {"$in": ["Варшава", "Астана", "Мадрид", "Прага"]},
                    "job": {"$in": ["Бухгалтер", "Психолог", "Продавец", "Повар"]},
                    "$or": [
                        {"age": {"$gt": 18, "$lt": 25}},
                        {"age": {"$gt": 50, "$lt": 65}},
                    ],
                }
            },
            {
                "$group": {
                    "_id": "result",
                    "min_salary": {"$min": "$salary"},
                    "max_salary": {"$max": "$salary"},
                    "avg_salary": {"$avg": "$salary"},
                }
            },
        ]
        data = collection.aggregate(stats)

        return list(data)

    def _get_random_data(self, collection):
        stats = [
            {"$match": {"age": {"$lt": 20}}},
            {
                "$group": {
                    "_id": "$job",
                    "min_salary": {"$min": "$salary"},
                    "max_salary": {"$max": "$salary"},
                    "avg_salary": {"$avg": "$salary"},
                }
            },
            {"$sort": {"avg_salary": -1}},
        ]
        data = collection.aggregate(stats)
        return list(data)


def main():
    jobs = Jobs("task_2_item.text")
    jobs.save_data()


if __name__ == "__main__":
    main()
