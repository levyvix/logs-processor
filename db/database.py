from sqlite3 import connect, Connection
from typing import List, Tuple, Optional
from config import DB_PATH
from loguru import logger


class Database:
    def __init__(self):
        self.connection: Optional[Connection] = None

    def __enter__(self):
        self.connection = connect(DB_PATH)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def transaction(self) -> Connection:
        """Context manager for database transactions"""
        return self.connection

    def create_table(self) -> None:
        """Create logs table if it doesn't exist"""
        try:
            with self.transaction() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level TEXT,
                        message TEXT,
                        timestamp TEXT
                    )
                    """,
                )
        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            raise

    def insert_logs(self, logs: List[Tuple[str, str, str]]) -> None:
        """Insert multiple log entries in a batch"""
        try:
            with self.transaction() as conn:
                conn.executemany(
                    """
                    INSERT INTO logs (level, message, timestamp)
                    VALUES (?, ?, ?)
                """,
                    logs,
                )
        except Exception as e:
            logger.error(f"Failed to insert logs: {e}")
            raise
