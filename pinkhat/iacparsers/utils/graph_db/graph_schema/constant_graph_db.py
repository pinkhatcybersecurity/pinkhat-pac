import ast

from kuzu import Connection
from loguru import logger

from iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ConstantGraphDb(BaseGraphDb):
    TABLE_NAME: str = "Constant"

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._constant_table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="col_offset", column_type="INT64"),
            Column(name="end_col_offset", column_type="INT64"),
            Column(name="end_lineno", column_type="INT64"),
            Column(name="kind", column_type="STRING"),
            Column(name="lineno", column_type="INT"),
            Column(name="type", column_type="STRING"),
            Column(name="n", column_type="STRING"),
            Column(name="s", column_type="STRING"),
            Column(name="value", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._constant_table.create()

    def add(self, value: ast.Constant, file_path: str):
        self._constant_table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "kind": value.kind,
                "lineno": value.lineno,
                "type": type(value.value).__name__,
                "n": value.n,
                "s": value.s,
                "value": value.value,
                "file_path": file_path,
            },
        )
