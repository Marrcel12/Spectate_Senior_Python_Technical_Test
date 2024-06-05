import os
import re
import sqlite3

from alembic import command
from alembic.config import Config

DATABASE_URL = "main.db"

from contextlib import contextmanager


@contextmanager
def create_new_db(url=DATABASE_URL):
    conn = get_connection(url=url, recreate=True)
    apply_migrations(url)
    try:
        yield conn
    finally:
        conn.close()


def delete_db(url):
    if os.path.exists(url):
        os.remove(url)


def get_connection(url=DATABASE_URL, recreate=False):
    if recreate:
        delete_db(url)
    conn = sqlite3.connect(url, check_same_thread=False)
    conn.create_function(
        "REGEXP", 2, lambda expr, item: re.search(expr, item) is not None
    )
    return conn


@contextmanager
def managed_cursor(conn):
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        conn.close()


def apply_migrations(url):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///./{url}")
    command.upgrade(alembic_cfg, "head")
