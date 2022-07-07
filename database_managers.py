from typing import Protocol, Any


class DatabaseManagerProtocol(Protocol):
    database: Any

    def get_table_data(self, table_name: str) -> Any: ...

    def save_table_data(self, table_name: str, data: Any) -> None: ...

    def close_session(self) -> None: ...


class ShelveDatabaseManager:
    def __init__(self, database: Any) -> None:
        self.database: Any = database

    def get_table_data(self, table_name: str) -> Any:
        return self.database.get(table_name)

    def save_table_data(self, table_name: str, data: Any) -> None:
        self.database[table_name] = data

    def close_session(self):
        self.database.close()
