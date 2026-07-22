import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', 5432))
        self.database = database or os.getenv('DB_NAME', 'studentroomsDB')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', 'postgres')

    def get_connection_params(self) -> Dict:
        return {
            'host': self.host,
            'port': self.port,
            'dbname': self.database,
            'user': self.user,
            'password': self.password,
            'connect_timeout': 10,
        }

    def __repr__(self) -> str:
        return f"DatabaseConfig(host={self.host}, database={self.database})"