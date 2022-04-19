import uuid
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created: datetime = field(default=datetime.now())
    modified: datetime = field(default=datetime.now())


@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    file_path: str
    rating: float
    type: str
    created: datetime = field(default=datetime.now())
    modified: datetime = field(default=datetime.now())


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created: datetime = field(default=datetime.now())
    modified: datetime = field(default=datetime.now())


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created: datetime = field(default=datetime.now())


@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created: datetime = field(default=datetime.now())


class SQLiteLoader:
    def __init__(self, connection) -> None:
        """Конструктор, создающий при инициализации объекта курсор и список таблиц"""
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.tables_info = [
            {"name": "genre"},
            {"name": "person"},
            {"name": "film_work"},
            {"name": "genre_film_work"},
            {"name": "person_film_work"},
        ]

    def load_batch(self, batch_size: int):
        """Генератор для получения следующего пакета записей из курсора"""
        data = self.cursor.fetchmany(batch_size)
        for row in data:
            yield row

    def get_table_rowcount(self, table_name: str):
        """Метод для получения количества строк в таблице"""
        select_table_rowcount_sql = "SELECT count(*) as cnt FROM {tn};".format(
            tn=table_name
        )
        rowcount = dict(self.cursor.execute(select_table_rowcount_sql).fetchone()).get(
            "cnt"
        )
        return rowcount

    def get_table_fields(self, table_name: str):
        """Метод для получения списка полей таблицы.
        В список не попадают поля 'created_at','updated_at'"""
        select_table_fields_sql = "SELECT pt.name FROM PRAGMA_TABLE_INFO('{tn}') AS pt WHERE pt.name NOT IN  ('created_at','updated_at');".format(
            tn=table_name
        )
        fields_data = [
            row_dict.get("name")
            for row_dict in [
                dict(row)
                for row in self.cursor.execute(select_table_fields_sql).fetchall()
            ]
        ]
        return fields_data

    def get_tables_info(self):
        """Метод для дополнения self.tables_info информацией о количестве записей и полях таблицы"""
        for table in self.tables_info:
            table["rowcount"] = self.get_table_rowcount(table.get("name"))
            table["fields"] = self.get_table_fields(table.get("name"))
        return self.tables_info

    def load_table(self, table_name: str):
        """Метод для получения всей таблицы в курсор из БД"""
        for ti in self.tables_info:
            if ti.get("name") == table_name:
                fields = ", ".join(ti.get("fields"))
        select_table_sql = "SELECT {tf} FROM {tn};".format(tf=fields, tn=table_name)
        self.cursor.execute(select_table_sql)

    def load_batch_list(self, table_name: str, bs: int):
        """Метод для получения списка объектов классов: FilmWork, Person, PersonFilmWork
        GenreFilmWork, Genre, в зависимости от параметра table_name"""
        if table_name == "genre":
            batch_data = [
                Genre(**row_dict)
                for row_dict in [dict(row) for row in self.load_batch(bs)]
            ]
            return batch_data

        if table_name == "genre_film_work":
            batch_data = [
                GenreFilmWork(**row_dict)
                for row_dict in [dict(row) for row in self.load_batch(bs)]
            ]
            return batch_data

        if table_name == "person_film_work":
            batch_data = [
                PersonFilmWork(**row_dict)
                for row_dict in [dict(row) for row in self.load_batch(bs)]
            ]
            return batch_data

        if table_name == "person":
            batch_data = [
                Person(**row_dict)
                for row_dict in [dict(row) for row in self.load_batch(bs)]
            ]
            return batch_data

        if table_name == "film_work":
            batch_data = [
                FilmWork(**row_dict)
                for row_dict in [dict(row) for row in self.load_batch(bs)]
            ]
            return batch_data
