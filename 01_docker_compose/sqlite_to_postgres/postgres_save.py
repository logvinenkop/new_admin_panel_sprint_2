from pkg_resources import to_filename
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_values


class PostgresSaver:
    def __init__(self, connection) -> None:
        """Конструктор, создающий при инициализации объекта курсор"""
        self.conn = connection
        self.cursor = self.conn.cursor()

    def get_table_rowcount(self, table_name: str):
        """Метод для получения количества строк в таблице"""
        select_table_rowcount_sql = "SELECT count(*) as cnt FROM {tn};".format(
            tn=table_name
        )
        self.cursor.execute(select_table_rowcount_sql)
        rowcount = self.cursor.fetchone()[0]
        return rowcount

    def save_data(self, table_name: str, table_fields: str, data: list):
        """Метод для вставки пакета записей в таблицу"""
        insert_sql = "INSERT INTO content.{tn} ({fields}) VALUES %s ON CONFLICT (id) DO NOTHING;".format(
            tn=table_name,
            fields=table_fields,
        )
        execute_values(self.cursor, insert_sql, data)
        self.conn.commit()
