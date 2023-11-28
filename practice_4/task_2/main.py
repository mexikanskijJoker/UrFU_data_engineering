import pickle as pkl
import sqlite3


DB_PATH = "/home/master/python/UrFU_data_engineering/practice_4/database.db"


class Table2:
    def __init__(self, file_name):
        self._file_name = file_name

    def db_connect(self):
        with sqlite3.connect(DB_PATH) as connection:
            db = connection.cursor()
        return db, connection

    def _create_table(self):
        conn = self.db_connect()
        conn[0].execute(
            """CREATE TABLE IF NOT EXISTS booksInfo (
            title TEXT PRIMARY KEY REFERENCES books (title),
            price INTEGER,
            place TEXT,
            date VARCHAR(11)
            ) """
        )
        conn[1].commit()

    def _get_file_data(self):
        with open(self._file_name, "rb") as file:
            data = pkl.load(file)

        return data

    def _set_table_data(self):
        conn = self.db_connect()
        file_data = self._get_file_data()
        rows = list(map(lambda book: tuple(book.values()), file_data))

        conn[0].executemany("INSERT OR IGNORE INTO booksInfo VALUES (?,?,?,?)", rows)
        conn[1].commit()

    def _join_request(self):
        conn = self.db_connect()
        rows = (
            conn[0]
            .execute(
                """SELECT b.title,
                b.author,
                b.genre,
                b.pages,
                b.published_year,
                b.isbn,
                b.rating,
                b.views,
                bf.price,
                bf.place,
                bf.date FROM books as b JOIN booksInfo as bf WHERE b.title = bf.title """
            )
            .fetchall()
        )
        result = []
        for row in rows:
            result.append(
                {
                    "title": row[0],
                    "author": row[1],
                    "genre": row[2],
                    "pages": row[3],
                    "published_year": row[4],
                    "isbn": row[5],
                    "rating": row[6],
                    "views": row[7],
                    "price": row[8],
                    "place": row[9],
                    "date": row[10],
                }
            )

        return result

    def _filtration_request_1(self):
        conn = self.db_connect()
        rows = (
            conn[0]
            .execute(
                """SELECT b.title, 
                b.author, 
                bf.price FROM books as b JOIN booksInfo as bf WHERE b.title = bf.title AND bf.price > 4500"""
            )
            .fetchall()
        )
        result = []
        for row in rows:
            result.append(
                {
                    "title": row[0],
                    "author": row[1],
                    "price": row[2],
                }
            )

        return result

    def _filtration_request_2(self):
        conn = self.db_connect()
        rows = (
            conn[0]
            .execute(
                """SELECT b.title, 
                b.author, 
                bf.place FROM books as b JOIN booksInfo as bf WHERE b.title = bf.title AND bf.place = 'online'"""
            )
            .fetchall()
        )
        result = []
        for row in rows:
            result.append(
                {
                    "title": row[0],
                    "author": row[1],
                    "place": row[2],
                }
            )

        return result


def main():
    table2 = Table2("task_2_var_88_subitem.pkl")
    table2._create_table()
    table2._set_table_data()
    print(table2._join_request())
    print(table2._filtration_request_1())
    print(table2._filtration_request_2())


if __name__ == "__main__":
    main()
