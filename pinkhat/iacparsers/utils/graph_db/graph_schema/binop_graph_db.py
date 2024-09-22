import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.attribute_graph_db import (
    AttributeGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import (
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class BinOpGraphDb(BaseGraphDb):
    TABLE_NAME: str = "BinOp"
    _rels = [
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Right",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Right",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": AttributeGraphDb.TABLE_NAME,
            "prefix": "Right",
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

    def add(self, value: ast.BinOp, file_path: str):
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
        left = self._get_stmt(value=value.left)
        if left:
            left.add(value=value.left, file_path=file_path)
            self._table.add_relation(
                to_table=left.TABLE_NAME,
                parent_value=value,
                child_value=value.left,
                file_path=file_path,
                prefix="Left",
            )
        right = self._get_stmt(value=value.right)
        if right:
            right.add(value=value.right, file_path=file_path)
            self._table.add_relation(
                to_table=right.TABLE_NAME,
                parent_value=value,
                child_value=value.right,
                file_path=file_path,
                prefix="Right",
            )
