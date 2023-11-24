import json
import sqlite3
import msgpack


VAR = 18


class Table:
    def __init__(self, file_name) -> None:
        self._file_name = file_name

    @staticmethod
    def _create_table() -> sqlite3.Cursor:
        with sqlite3.connect("my_database.db") as connection:
            db = connection.cursor()
        db.execute(
            """CREATE TABLE IF NOT EXISTS Books (
            title TEXT PRIMARY KEY,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            pages INTEGER,
            published_year INTEGER,
            isbn TEXT,
            rating FLOAT,
            views INTEGER
            )"""
        )
        connection.commit()

    @staticmethod
    def _get_category_freq() -> list:
        with sqlite3.connect("my_database.db") as connection:
            db = connection.cursor()
        res = db.execute(
            """SELECT genre, count(*) FROM books GROUP BY genre"""
        ).fetchall()
        return res

    def _get_file_data(self) -> list[dict]:
        with open(self._file_name, "rb") as data_file:
            byte_data = data_file.read()
            data = msgpack.unpackb(byte_data)
            values = list(map(lambda i: tuple(i.values()), data))

        return values

    @staticmethod
    def _get_filetered_param():
        with sqlite3.connect("my_database.db") as connection:
            db = connection.cursor()
        rows = db.execute(
            """SELECT * FROM books WHERE published_year > 1960 ORDER BY published_year LIMIT ? """,
            [VAR + 10],
        ).fetchall()
        data = []
        for row in rows:
            data.append(
                {
                    "title": row[0],
                    "author": row[1],
                    "genre": row[2],
                    "pages": row[3],
                    "published_year": row[4],
                    "isbn": row[5],
                    "rating": row[6],
                    "views": row[7],
                }
            )
        return data

    @staticmethod
    def _get_int_parameters() -> dict:
        with sqlite3.connect("my_database.db") as connection:
            db = connection.cursor()
        res = db.execute(
            """SELECT SUM(views), MIN(views), MAX(views), AVG(views) FROM books"""
        ).fetchone()
        return {"sum": res[0], "min": res[1], "max": res[2], "avg": res[3]}

    @staticmethod
    def _get_sorted_param() -> list[dict]:
        with sqlite3.connect("my_database.db") as connection:
            db = connection.cursor()
        rows = (
            db.execute("""SELECT * FROM books ORDER BY pages LIMIT ?""", [VAR + 10])
        ).fetchall()
        data = []
        for row in rows:
            data.append(
                {
                    "title": row[0],
                    "author": row[1],
                    "genre": row[2],
                    "pages": row[3],
                    "published_year": row[4],
                    "isbn": row[5],
                    "rating": row[6],
                    "views": row[7],
                }
            )
        return data

    def _save_data(self) -> None:
        pages = self._get_sorted_param()
        years = self._get_filetered_param()
        with open("sort_pages.json", "w", encoding="UTF-8") as json_file:
            json_data = json.dumps(pages, ensure_ascii=False, indent=2)
            json_file.write(json_data)
        with open("filtered_publ_year.json", "w", encoding="UTF-8") as json_file:
            json_data = json.dumps(years, ensure_ascii=False, indent=2)
            json_file.write(json_data)

    def _set_data_table(self) -> sqlite3.Cursor:
        data = self._get_file_data()
        with sqlite3.connect("my_database.db") as connection:
            db = connection.cursor()
        db.executemany("INSERT OR IGNORE INTO books VALUES (?,?,?,?,?,?,?,?)", data)
        connection.commit()


def main() -> None:
    table = Table("task_1_var_88_item.msgpack")
    table._create_table()
    table._set_data_table()
    table._save_data()
    print(table._get_int_parameters())
    print(table._get_category_freq())


if __name__ == "__main__":
    main()
