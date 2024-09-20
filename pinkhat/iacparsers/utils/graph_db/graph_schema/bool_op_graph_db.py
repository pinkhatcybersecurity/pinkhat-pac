import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.compare_graph_db import CompareGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class BoolOpGraphDb(BaseGraphDb):
    TABLE_NAME: str = "BoolOp"
    _rels = [
        {
            "to_table": CompareGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="col_offset", column_type="INT64"),
            Column(name="end_col_offset", column_type="INT64"),
            Column(name="end_lineno", column_type="INT64"),
            Column(name="lineno", column_type="INT"),
            Column(name="op", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._table.create()

    def create_rel(self):
        for rel in self._rels:
            self._table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.BoolOp, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "op": type(value.op).__name__,
                "lineno": value.lineno,
                "file_path": file_path,
            },
        )
        for val in value.values:
            stmt = self._get_stmt(value=val)
            if stmt:
                stmt.add(value=val, file_path=file_path)
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=val,
                    file_path=file_path,
                    prefix="Value",
                )
