import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.bool_op_graph_db import BoolOpGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.compare_graph_db import CompareGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.expr_graph_db import ExprGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class IfGraphDb(BaseGraphDb):
    TABLE_NAME = "If"
    _rels = [
        {
            "to_table": ExprGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ExprGraphDb.TABLE_NAME,
            "prefix": "OrElse",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TABLE_NAME,
            "prefix": "OrElse",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": CompareGraphDb.TABLE_NAME,
            "prefix": "If",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": BoolOpGraphDb.TABLE_NAME,
            "prefix": "If",
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

    def add(self, value: ast.If, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._parse_test(value=value, file_path=file_path)
        self._parse_body(value=value, file_path=file_path)
        or_else: ast.If
        for or_else in value.orelse:
            stmt = self._get_stmt(value=or_else)
            if stmt:
                stmt.add(value=or_else, file_path=file_path)
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=or_else,
                    file_path=file_path,
                    prefix="OrElse",
                )

    def _parse_body(self, value: ast.If, file_path: str):
        for body in value.body:
            stmt = self._get_stmt(value=body)
            if stmt:
                stmt.add(value=body, file_path=file_path)
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=body,
                    file_path=file_path,
                    prefix="Body",
                )

    def _parse_test(self, value: ast.If, file_path: str):
        stmt = self._get_stmt(value=value.test)
        if stmt:
            stmt.add(value=value.test, file_path=file_path)
            self._table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=value.test,
                file_path=file_path,
                prefix="If",
            )
