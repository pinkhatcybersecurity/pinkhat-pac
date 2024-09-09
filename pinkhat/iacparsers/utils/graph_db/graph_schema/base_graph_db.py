from kuzu import Connection
from loguru import logger


class BaseGraphDb:
    def __init__(self, conn: Connection):
        self._conn: Connection = conn
        self._stmt = None
        self._expr = None

    def _get_stmt(self, value):
        if not value:
            return None
        stmt = self._stmt.get(type(value), self._expr.get(type(value)))
        if stmt:
            return stmt
        logger.error(f"Unknown type {type(value)}")
