import psycopg2
import sqlite3
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from migrate_logger import log

my_log = log()


@contextmanager
def sqlite_conn_context(db_path: str):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        my_log.info("Connected to SQLite DB")
        yield conn
    except Exception as e:
        my_log.error("Возника ошибка: {er}".format(er=e))
    finally:
        conn.close()
        my_log.info("Disconnected from SQLite")


@contextmanager
def pg_conn_context(dsl):
    try:
        conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        my_log.info("Connected to Postgres")
        yield conn
    except Exception as e:
        my_log.error("Возника ошибка: {er}".format(er=e))
    finally:
        conn.close()
        my_log.info("Disconnected from Postgres")
