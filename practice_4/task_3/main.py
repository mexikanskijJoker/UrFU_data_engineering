import csv
import json
import msgpack
import re
import sqlite3


DB_PATH = "/home/master/python/UrFU_data_engineering/practice_4/database.db"
VAR = 88


class SongsTable:
    def __init__(self, file1, file2) -> None:
        self.csv_file = file1
        self.msgpack_file = file2

    def db_connect(self):
        with sqlite3.connect(DB_PATH) as connection:
            db = connection.cursor()

        return db, connection

    def _create_table(self):
        conn = self.db_connect()
        conn[0].execute(
            """CREATE TABLE IF NOT EXISTS songs (
            artist TEXT,
            song TEXT,
            duration_ms TEXT,
            year VARCHAR(4),
            tempo FLOAT,
            genre TEXT,
            mode TEXT,
            speechiness FLOAT,
            acousticness FLOAT,
            instrumentalness FLOAT,
            energy FLOAT,
            key INTEGER,
            loudness FLOAT
            )"""
        )
        conn[1].commit()

    def _get_csv_data(self):
        with open(self.csv_file, "r") as file:
            reader = csv.reader(file, delimiter=";")
            csv_data = [
                tuple(
                    map(
                        lambda value: float(value)
                        if re.fullmatch(r"\d+\.\d+", value) != None
                        else value,
                        row,
                    )
                )
                for row in reader
                if row != []
            ]
        return csv_data[1 : len(csv_data) + 1]

    def _get_msgpack_data(self):
        with open(self.msgpack_file, "rb") as file:
            byte_data = file.read()
            msg_data = msgpack.unpackb(byte_data)
        values = list(
            map(
                lambda song: tuple(
                    map(
                        lambda value: float(value)
                        if re.fullmatch(r"\d+\.\d+", value) != None
                        else value,
                        song.values(),
                    )
                ),
                msg_data,
            )
        )
        return values

    def _set_table_data(self):
        csv_data, msg_data = self._get_csv_data(), self._get_msgpack_data()
        conn = self.db_connect()
        conn[0].executemany(
            """INSERT INTO songs
                (artist,
                song,
                duration_ms,
                year,
                tempo,
                genre,
                mode,
                speechiness,
                acousticness,
                instrumentalness
                )
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
            msg_data,
        )
        conn[1].commit()

        conn[0].executemany(
            """INSERT INTO songs
                (artist,
                song,
                duration_ms,
                year,
                tempo,
                genre,
                energy,
                key,
                loudness)
                VALUES (?,?,?,?,?,?,?,?,?)""",
            csv_data,
        )
        conn[1].commit()

    def _get_sorted_and_filtered_rows(self):
        conn = self.db_connect()
        sorted_rows = (
            conn[0]
            .execute("""SELECT * FROM songs ORDER BY tempo LIMIT ?""", [VAR + 10])
            .fetchall()
        )
        sorted_data = []
        for row in sorted_rows:
            sorted_data.append(
                {
                    "artist": row[0],
                    "song": row[1],
                    "duration_ms": row[2],
                    "year": row[3],
                    "tempo": row[4],
                    "genre": row[5],
                    "mode": row[6],
                    "speechiness": row[7],
                    "acousticness": row[8],
                    "instrumental": row[9],
                    "energy": row[10],
                    "key": row[11],
                    "loudness": row[12],
                }
            )

        filtered_rows = (
            conn[0]
            .execute(
                """SELECT * FROM songs WHERE tempo > 200 ORDER BY tempo LIMIT ?  """,
                [VAR + 15],
            )
            .fetchall()
        )
        filtered_data = []
        for row in filtered_rows:
            filtered_data.append(
                {
                    "artist": row[0],
                    "song": row[1],
                    "duration_ms": row[2],
                    "year": row[3],
                    "tempo": row[4],
                    "genre": row[5],
                    "mode": row[6],
                    "speechiness": row[7],
                    "acousticness": row[8],
                    "instrumental": row[9],
                    "energy": row[10],
                    "key": row[11],
                    "loudness": row[12],
                }
            )
        return sorted_data, filtered_data

    def _get_numeric_params(self):
        conn = self.db_connect()
        result = (
            conn[0]
            .execute(
                """SELECT SUM(speechiness), MIN(speechiness), MAX(speechiness), AVG(speechiness) FROM songs"""
            )
            .fetchone()
        )
        return {"sum": result[0], "min": result[1], "max": result[2], "avg": result[3]}

    def _get_column_frequency(self):
        conn = self.db_connect()
        result = (
            conn[0]
            .execute("""SELECT genre, COUNT(genre) FROM songs GROUP BY genre""")
            .fetchall()
        )
        return sorted(result, key=lambda genre: genre[1], reverse=True)

    def save_data(self):
        data = self._get_sorted_and_filtered_rows()
        with open("sorted_data.json", "w", encoding="UTF-8") as sorted_file:
            sorted_data = json.dumps(data[0], ensure_ascii=False, indent=2)
            sorted_file.write(sorted_data)
        with open("sorted_and_filtered_data.json", "w") as filtered_file:
            filtered_data = json.dumps(data[0], ensure_ascii=False, indent=2)
            filtered_file.write(filtered_data)


def main():
    table = SongsTable("task_3_var_88_part_2.csv", "task_3_var_88_part_1.msgpack")
    table._create_table()
    table._set_table_data()
    print(table._get_numeric_params())
    print(table._get_column_frequency())
    table.save_data()


if __name__ == "__main__":
    main()
