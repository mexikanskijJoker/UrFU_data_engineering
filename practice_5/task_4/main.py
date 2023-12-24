from pymongo import MongoClient
import csv
import json
from bson.json_util import dumps
import os


def read_csv_data(filename: str) -> list:
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        rows = [row for row in reader]
        result = []
        for row in rows[1:]:
            item = dict(zip(rows[0], row))
            for key in item.keys():
                if key not in ["country_code", "sex"]:
                    item[key] = float(item[key])
            result.append(item)
    return result


def read_json_data(filename):
    with open(filename, encoding="utf-8") as file:
        result = json.load(file)
    return result


def insert_data(collection, data):
    collection.insert_many(data)


def select_top(collection, year):
    cursor = collection.find({}, limit=10).sort({f"{year}": -1})
    result = list(cursor)
    with open(
        f"./results/select_queries/top_{year}.json", "w", encoding="utf-8"
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def select_by_sex(collection):
    cursor = collection.find({"sex": "Female"})
    result = list(cursor)
    with open(
        "./results/select_queries/select_by_sex.json", "w", encoding="utf-8"
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def select_by_country(collection):
    cursor = collection.find({"country_code": {"$in": ["RO", "CZ", "DE", "FR"]}})
    result = list(cursor)
    with open(
        "./results/select_queries/select_by_country.json", "w", encoding="utf-8"
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def complex_selection(collection):
    query = {
        "country_code": {"$nin": ["RO", "CZ", "DE", "FR"]},
        "sex": "Male",
        "$or": [{"2019": {"$lt": 6}}, {"2019": {"$gt": 9.5}}],
    }
    cursor = collection.find(query)
    result = list(cursor)
    with open(
        "./results/select_queries/complex_selection.json", "w", encoding="utf-8"
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def count_documents(collection):
    query = [
        {"$match": {"2019": {"$gt": 12}}},
        {
            "$group": {
                "_id": "$sex",
                "count": {"$sum": 1},
            }
        },
    ]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open(
        f"./results/aggregation_queries/count_documents.json", "w", encoding="utf-8"
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def get_hly_stat(collection, year):
    query = [
        {
            "$group": {
                "_id": f"result (year {year})",
                "max_hly": {"$max": f"${year}"},
                "min_hly": {"$min": f"${year}"},
                "average_hly": {"$avg": f"${year}"},
            }
        },
        {"$sort": {f"{year}": -1}},
    ]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open(
        f"./results/aggregation_queries/hly_stat_{year}.json", "w", encoding="utf-8"
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def get_hly_stat_by_sex(collection, year):
    query = [
        {
            "$group": {
                "_id": "$sex",
                "max_hly": {"$max": f"${year}"},
                "min_hly": {"$min": f"${year}"},
                "average_hly": {"$avg": f"${year}"},
            }
        }
    ]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open(
        f"./results/aggregation_queries/hly_stat_by_sex_{year}.json",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(dumps(result, ensure_ascii=False))


def update_by_country(collection, year, country_code):
    filter = {"country_code": f"{country_code}"}
    update = {"$inc": {f"{year}": 1}}
    result = collection.update_one(filter, update)
    print(
        f"Count of modified documents (increment data in {year}, country = {country_code}): ",
        result.modified_count,
    )


def update_complex(collection):
    filter = {"sex": "Male", "country_code": {"$nin": ["RO", "CZ", "DE", "FR"]}}
    update = {"$inc": {"2019": -1}}
    result = collection.update_many(filter, update)
    print(
        f"Count of modified documents (by complex predicate): ", result.modified_count
    )


def delete_by_country_list(collection):
    query = {"country_code": {"$in": ["FR", "HR", "HU"]}}
    result = collection.delete_many(query)
    print("Count of deleted documents (deleted by country): ", result.deleted_count)


def delete_by_predicate(collection):
    query = {"$or": [{"2019": {"$lt": 5}}, {"2019": {"$gt": 13}}]}
    result = collection.delete_many(query)
    print("Count of deleted documents (deleted by predicate): ", result.deleted_count)


client = MongoClient()
db = client["practice_5"]

data = read_csv_data("HLY_at_65_males.csv") + read_json_data("HLY_at_65_females.json")
insert_data(db.task_4, data)
collection = db.task_4

os.makedirs("./results/select_queries", exist_ok=True)
os.makedirs("./results/aggregation_queries", exist_ok=True)

select_top(collection, 2019)
select_top(collection, 2011)
select_by_sex(collection)
select_by_country(collection)
complex_selection(collection)

get_hly_stat(collection, 2012)
get_hly_stat(collection, 2015)
get_hly_stat_by_sex(collection, 2010)
get_hly_stat_by_sex(collection, 2019)
count_documents(collection)

update_by_country(collection, 2019, "AT")
update_by_country(collection, 2013, "DE")
update_complex(collection)
delete_by_country_list(collection)
delete_by_predicate(collection)
