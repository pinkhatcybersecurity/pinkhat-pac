import ast

from kuzu import Connection

from iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from iacparsers.utils.graph_db.graph_schema.constant_graph_db import ConstantGraphDb
from iacparsers.utils.graph_db.graph_schema.list_graph_db import ListGraphDb
from iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class CompareGraphDb(BaseGraphDb):
    TABLE_NAME: str = "Compare"
    _rels = [
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Comparator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ListGraphDb.TABLE_NAME,
            "prefix": "Comparator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Comparator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Left",
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

    def add(self, value: ast.Compare, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._parse_left(value=value, file_path=file_path)
        self._parse_op(value=value, file_path=file_path)
        self._parse_comparator(value, file_path)

    def _parse_comparator(self, value: ast.Compare, file_path: str):
        for comparator in value.comparators:
            stmt = self._get_stmt(value=comparator)
            if stmt:
                stmt.add(value=comparator, file_path=file_path)
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=comparator,
                    file_path=file_path,
                    prefix="Comparator",
                )

    def _parse_op(self, value: ast.Compare, file_path: str):
        for op in value.ops:
            stmt = self._get_stmt(value=op)
            if stmt:
                stmt.add(value=op, file_path=file_path)
                # self._table.add_relation(
                #     to_table=stmt.TABLE_NAME,
                #     parent_value=value,
                #     child_value=op,
                #     file_path=file_path,
                #     prefix="Op",
                # )

    def _parse_left(self, value: ast.Compare, file_path: str):
        stmt = self._get_stmt(value=value.left)
        if stmt:
            stmt.add(value.left, file_path=file_path)
            self._table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=value.left,
                file_path=file_path,
                prefix="Left",
            )
