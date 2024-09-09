import ast

from kuzu import Connection

from iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from iacparsers.utils.graph_db.graph_schema.expr_graph_db import ExprGraphDb
from iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ForGraphDb(BaseGraphDb):
    TABLE_NAME: str = "For"
    _rels = [
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Iter",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Target",
            "extra_fields": "lineno INT, file_path STRING",
        },
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
            Column(name="type_comment", column_type="STRING"),
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

    def add(self, value: ast.For, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "type_comment": value.type_comment,
                "file_path": file_path,
            }
        )
        self._parse_iter(value=value, file_path=file_path)
        self._parse_target(value=value, file_path=file_path)
        self._parse_body(value=value, file_path=file_path)
        self._parse_or_else(value=value, file_path=file_path)

    def _parse_or_else(self, value: ast.For, file_path: str):
        for orelse in value.orelse:
            stmt = self._get_stmt(value=orelse)
            if stmt:
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=orelse,
                    file_path=file_path,
                    prefix="OrElse",
                )

    def _parse_body(self, value: ast.For, file_path: str):
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

    def _parse_target(self, value: ast.For, file_path: str):
        stmt = self._get_stmt(value=value.target)
        if stmt:
            stmt.add(value=value.target, file_path=file_path)
            self._table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=value.target,
                file_path=file_path,
                prefix="Target",
            )

    def _parse_iter(self, value: ast.For, file_path: str):
        stmt = self._get_stmt(value=value.iter)
        if stmt:
            stmt.add(value=value.iter, file_path=file_path)
            self._table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=value.iter,
                file_path=file_path,
                prefix="Iter",
            )
