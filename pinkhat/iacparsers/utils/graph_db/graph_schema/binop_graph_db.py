import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class BinOpGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.BinOp.value
    _rels = {
        "prefix": {
            "Left": [
                TableName.Attribute.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Tuple.value,
            ],
            "Right": [
                TableName.Attribute.value,
                TableName.Constant.value,
                TableName.Name.value,
            ],
        },
        "extra_fields": "lineno INT, file_path STRING",
    }

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

    def initialize(self, stmt: dict):
        self._stmt = stmt
        self._table.create()

    def create_rel(self):
        for prefix, tables in self._rels.get("prefix", {}).items():
            self._table.create_relationship_group(
                to_table=tables,
                prefix=prefix,
                extra_fields=self._rels.get("extra_fields"),
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
        if left := self._get_stmt(value=value.left):
            left.add(value=value.left, file_path=file_path)
            self._table.add_relation_group(
                stmt=self._stmt,
                parent_value=value,
                child_value=[value.left],
                file_path=file_path,
                prefix="Left",
                extra_field={},
            )
        if right := self._get_stmt(value=value.right):
            right.add(value=value.right, file_path=file_path)
            self._table.add_relation_group(
                stmt=self._stmt,
                parent_value=value,
                child_value=[value.right],
                file_path=file_path,
                prefix="Right",
                extra_field={},
            )
