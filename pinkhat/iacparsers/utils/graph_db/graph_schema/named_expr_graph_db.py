import ast

from kuzu import Connection
from loguru import logger

from pinkhat.iacparsers.utils.graph_db.graph_schema import (
    CallGraphDb,
    NameGraphDb,
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.arg_graph_db import ArgGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class NamedExprGraphDb(BaseGraphDb):
    """
    Named Expression Python description can be found in the link below:
    https://peps.python.org/pep-0572/
    """

    TABLE_NAME = "NamedExpr"
    _rels = [
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Target",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
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

    def add(self, value: ast.NamedExpr, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._add_relationship(
            parent_value=value,
            child_value=value.value,
            file_path=file_path,
            prefix="Value",
        )
        self._add_relationship(
            parent_value=value,
            child_value=value.target,
            file_path=file_path,
            prefix="Target",
        )
