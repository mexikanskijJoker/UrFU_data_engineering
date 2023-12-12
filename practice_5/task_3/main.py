import pickle

from pymongo import MongoClient


class Jobs:
    def __init__(self, file):
        self.file = file

    def execute_all(self):
        collection = self._connect()
        data = self._get_file_data()
        self._set_db_data(collection, data)
        self._delete_by_salary(collection)
        self._update_age(collection)
        self._update_salary_by_job(collection)
        self._update_salary_by_city(collection)
        self._update_salary(collection)
        self._delete_by_age(collection)

    def _connect(self):
        client = MongoClient()
        db = client["practice_5"]
        return db.jobs

    def _get_file_data(self):
        with open(self.file, "rb") as file:
            data = pickle.load(file)

        return data

    def _set_db_data(self, collection, data):
        collection.insert_many(data)

    def _delete_by_salary(self, collection):
        condition = {"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]}
        collection.delete_many(condition)

    def _update_age(self, collection):
        condition = {"$inc": {"age": 1}}
        collection.update_many({}, condition)

    def _update_salary_by_job(self, collection):
        filter = {"job": {"$in": ["Косметолог", "Повар", "Программист", "Медсестра"]}}
        update = {"$mul": {"salary": 1.05}}
        collection.update_many(filter, update)

    def _update_salary_by_city(self, collection):
        filter = {"city": {"$in": ["Астана", "Варшава", "Таллин", "Вильнюс"]}}
        update = {"$mul": {"salary": 1.07}}
        collection.update_many(filter, update)

    def _update_salary(self, collection):
        filter = {
            "city": {"$in": ["Хельсинки", "Москва", "Рига", "Тбилиси"]},
            "job": {"$in": ["Повар", "Медсестра", "Программист"]},
            "$or": [{"age": {"$gt": 19}}, {"age": {"$lt": 30}}],
        }
        update = {"$mul": {"salary": 1.1}}
        collection.update_many(filter, update)

    def _delete_by_age(self, collection):
        query = {"job": "Менеджер", "$or": [{"age": {"$lt": 30}}, {"age": {"$gt": 40}}]}
        collection.delete_many(query)


def main():
    jobs = Jobs("task_3_item.pkl")
    jobs.execute_all()


if __name__ == "__main__":
    main()
