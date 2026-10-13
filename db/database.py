"""Подключение к базе SQLite сервиса записи к врачу."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "doctor_appointment.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection():
    """Открыть соединение и включить проверку внешних ключей.

    sqlite3.Row позволяет обращаться к полям результата по имени
    и в Python, и в шаблоне Django.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def fetch_all(query, params=()):
    """Выполнить запрос и вернуть все строки."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def fetch_one(query, params=()):
    """Выполнить запрос и вернуть первую строку или None."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()


def apply_schema():
    """Создать таблицы по файлу sql/schema.sql."""
    script = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(script)
        conn.commit()
    finally:
        conn.close()
