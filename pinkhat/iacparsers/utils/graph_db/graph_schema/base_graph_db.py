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

    def create_rel(self):
        # logger.info(f"Adding relationships for table {self.TABLE_NAME}")
        if not hasattr(self, "_rels"):
            return
        for prefix, tables in self._rels.get("prefix", {}).items():
            values, extra_fields = (
                (tables.get("rels"), tables.get("extra_fields"))
                if type(tables) == dict
                else (tables, self._rels.get("extra_fields"))
            )
            self._table.create_relationship_group(
                to_table=values,
                prefix=prefix,
                extra_fields=extra_fields,
            )

    def _save_relationship(
        self,
        parent_value,
        child_value,
        file_path: str,
        prefix: str,
        extra_field: dict = None,
    ):
        if stmt := self._get_stmt(value=child_value):
            p_id = self._table.p_id()
            stmt.add(value=child_value, file_path=file_path)
            self._table.save_relation(
                table=stmt.TABLE_NAME,
                parent_value=parent_value,
                child_value=child_value,
                p_id=p_id,
                c_id=stmt.p_id(),
                file_path=file_path,
                prefix=prefix,
                extra_field=extra_field,
            )

    def _save_relationship_only(
        self,
        parent_value,
        child_value,
        file_path: str,
        prefix: str,
        extra_field: dict = None,
    ):
        if stmt := self._get_stmt(value=child_value):
            self._table.save_relation(
                table=stmt.TABLE_NAME,
                parent_value=parent_value,
                child_value=child_value,
                p_id=self._table.p_id(),
                c_id=stmt.p_id(),
                file_path=file_path,
                prefix=prefix,
                extra_field=extra_field,
            )

    def close_fd(self):
        self._table.close_fd()
