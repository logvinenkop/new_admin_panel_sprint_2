import sqlite3
import sqlite_load
import postgres_save
import os
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from dataclasses import asdict, astuple
from contexts import pg_conn_context, sqlite_conn_context
from migrate_logger import log

load_dotenv()
my_log = log()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    batch_size = int(os.environ.get("BATCH_SIZE"))
    sqlite_loader = sqlite_load.SQLiteLoader(connection)
    sqlite_tables = sqlite_loader.get_tables_info()
    postgres_saver = postgres_save.PostgresSaver(pg_conn)
    for table in sqlite_tables:
        t_name = table.get("name")
        my_log.debug(t_name)
        sqlite_loader.load_table(t_name)
        i = 0
        while i <= table.get("rowcount") // batch_size:
            batch = sqlite_loader.load_batch_list(t_name, batch_size)
            my_log.info(
                "Batch {bn} of {bs} rows".format(bn=str(i + 1), bs=str(len(batch)))
            )
            batch_fields = ", ".join(asdict(batch[0]).keys())
            data = [astuple(row) for row in batch]

            postgres_saver.save_data(t_name, batch_fields, data)
            my_log.info("Batch saved to table: " + t_name)

            i += 1


if __name__ == "__main__":
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", default="127.0.0.1"),
        "port": os.environ.get("DB_PORT", default=5432),
    }
    with sqlite_conn_context(
        os.environ.get("SQLITE_DB_PATH")
    ) as sqlite_conn, pg_conn_context(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
