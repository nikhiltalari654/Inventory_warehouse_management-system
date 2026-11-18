import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "inventory.db"
)

SCHEMA = os.path.join(
    BASE_DIR,
    "app",
    "schema.sql"
)


def get_connection():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def create_tables():
    connection = get_connection()

    with open(SCHEMA, "r") as file:
        schema = file.read()

    connection.executescript(schema)

    connection.commit()
    connection.close()