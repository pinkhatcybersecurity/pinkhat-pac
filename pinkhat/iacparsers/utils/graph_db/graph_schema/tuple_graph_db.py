import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import (
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.named_expr_graph_db import (
    NamedExprGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class TupleGraphDb(BaseGraphDb):
    TABLE_NAME = "Tuple"
    _rels = [
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Dim",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Elt",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Dim",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Elt",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Elt",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Dim",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NamedExprGraphDb.TABLE_NAME,
            "prefix": "Dim",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NamedExprGraphDb.TABLE_NAME,
            "prefix": "Elt",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._tuple_table = Table(
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
        self._tuple_table.create()

    def create_rel(self):
        for rel in self._rels:
            self._tuple_table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.Tuple, file_path: str):
        self._tuple_table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            },
        )
        for dim in value.dims:
            expr = self._get_stmt(value=dim)
            if expr:
                expr.add(value=dim, file_path=file_path)
                self._tuple_table.add_relation(
                    to_table=expr.TABLE_NAME,
                    parent_value=value,
                    child_value=dim,
                    file_path=file_path,
                    prefix="Dim",
                )
        for elt in value.elts:
            expr = self._get_stmt(value=elt)
            if expr:
                expr.add(value=elt, file_path=file_path)
                self._tuple_table.add_relation(
                    to_table=expr.TABLE_NAME,
                    parent_value=value,
                    child_value=elt,
                    file_path=file_path,
                    prefix="Elt",
                )
