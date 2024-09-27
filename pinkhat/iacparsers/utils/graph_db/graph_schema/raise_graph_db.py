import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class RaiseGraphDb(BaseGraphDb):
    TABLE_NAME: str = "Raise"
    _rels = [
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Exc",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Exc",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="cause", column_type="STRING"),
            Column(name="col_offset", column_type="INT64"),
            Column(name="end_col_offset", column_type="INT64"),
            Column(name="end_lineno", column_type="INT64"),
            Column(name="lineno", column_type="INT"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict):
        self._stmt = stmt
        self._table.create()

    def create_rel(self):
        for rel in self._rels:
            self._table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.Raise, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._parse_exc(value=value, file_path=file_path)

    def _parse_exc(self, value: ast.Raise, file_path: str):
        stmt = self._get_stmt(value=value.exc)
        if stmt:
            stmt.add(value=value.exc, file_path=file_path)
            self._table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=value.exc,
                file_path=file_path,
                prefix="Exc",
            )
