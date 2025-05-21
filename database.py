import sqlite3
from contextlib import closing
from typing import List, Tuple
from config import DB_NAME

class Database:
    @staticmethod
    def init_db():
        with closing(sqlite3.connect(DB_NAME)) as conn:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS events (
                        user_id INTEGER,
                        event_id TEXT,
                        date TEXT,
                        text TEXT,
                        remind_time TEXT,
                        PRIMARY KEY (user_id, event_id)
                    )
                """)

    @staticmethod
    def execute_query(query: str, params: tuple = (), fetch: bool = False):
        with closing(sqlite3.connect(DB_NAME)) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return cursor.rowcount