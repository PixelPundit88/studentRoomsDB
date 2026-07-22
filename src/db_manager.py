from typing import List, Dict, Optional, Tuple, Protocol
import psycopg
from src.config import DatabaseConfig


class DatabaseInterface(Protocol):
    def connect(self) -> None: ...
    def execute(self, query: str, params: Optional[Tuple] = None) -> None: ...
    def executemany(self, query: str, params_list: List[Tuple]) -> int: ...
    def fetchall(self, query: str, params: Optional[Tuple] = None) -> List[Dict]: ...
    def fetchone(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict]: ...
    def close(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None
        self.cursor = None
        self._connected = False

    def connect(self) -> None:
        try:
            params = self.config.get_connection_params()
            self.connection = psycopg.connect(**params)
            self.cursor = self.connection.cursor()
            self._connected = True
            print(f"Connected to PostgreSQL database: {self.config.database}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}") from e

    def execute(self, query: str, params: Optional[Tuple] = None) -> None:
        if not self._connected:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.execute(query, params)
        self.connection.commit()

    def executemany(self, query: str, params_list: List[Tuple]) -> int:
        if not self._connected:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.executemany(query, params_list)
        self.connection.commit()
        return len(params_list)

    def fetchall(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        if not self._connected:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.execute(query, params)
        columns = [desc.name for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def fetchone(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict]:
        if not self._connected:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        if row:
            columns = [desc.name for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self._connected = False
        print("Database connection closed")

    def is_connected(self) -> bool:
        return self._connected

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()