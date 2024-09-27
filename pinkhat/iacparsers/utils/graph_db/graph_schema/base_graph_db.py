from kuzu import Connection
from loguru import logger


class BaseGraphDb:
    def __init__(self, conn: Connection):
        self._conn: Connection = conn
        self._stmt = None
        self._table = None

    def _get_stmt(self, value):
        if not value:
            return None
        stmt = self._stmt.get(type(value))
        if stmt:
            return stmt
        logger.error(f"Unknown type {type(value)}")

    def _add_relationship(self, parent_value, child_value, file_path: str, prefix: str):
        stmt = self._get_stmt(value=child_value)
        if stmt:
            stmt.add(child_value, file_path=file_path)
            self._table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=parent_value,
                child_value=child_value,
                file_path=file_path,
                prefix=prefix,
            )
