import csv
import os

from kuzu import Connection
from loguru import logger


class BaseGraphDb:
    def __init__(self, conn: Connection):
        self._conn: Connection = conn
        self._stmt = None
        self._table = None

    def initialize(self, stmt: dict):
        self._stmt = stmt
        self._table.create()

    def p_id(self):
        return self._table.p_id()

    def _get_stmt(self, value):
        if not value:
            return None
        stmt = self._stmt.get(type(value))
        if stmt:
            return stmt
        logger.error(f"Unknown type {type(value)}")

    def _save_relationship(
        self, parent_value, child_value, file_path: str, prefix: str
    ):
        if stmt := self._get_stmt(value=child_value):
            stmt.add(value=child_value, file_path=file_path)
            self._table.save_relation(
                table=stmt.TABLE_NAME,
                parent_value=parent_value,
                child_value=child_value,
                c_id=stmt.p_id(),
                file_path=file_path,
                prefix=prefix,
            )
