import ast
import math

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class CompareGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.Compare.value

    _rels = {
        "prefix": {
            "Left": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
                TableName.Tuple.value,
                TableName.Subscript.value,
            ],
            "Comparator": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.List.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
                TableName.Tuple.value,
                TableName.Set.value,
                TableName.Subscript.value,
            ],
            "Op": {
                "rels": [
                    TableName.Attribute.value,
                    TableName.Call.value,
                    TableName.Constant.value,
                    TableName.List.value,
                    TableName.Name.value,
                    TableName.NamedExpr.value,
                    TableName.Tuple.value,
                    TableName.Set.value,
                    TableName.Subscript.value
                ],
                "extra_fields": "index INT, lineno INT, op STRING, file_path STRING",
            },
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
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.Compare, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._parse_left(value=value, file_path=file_path)
        self._parse_comparator(value=value, file_path=file_path)

    def _parse_comparator(self, value: ast.Compare, file_path: str):
        index = 0.5
        for comparator in value.comparators:
            self._save_relationship(
                parent_value=value,
                child_value=comparator,
                file_path=file_path,
                prefix="Comparator",
            )
            # Collect the rest of the elements. Go through the list - 1.
            # The last element is not assigned to anything. So, it can be skipped.
            ceil = math.ceil(index)
            self._save_relationship(
                parent_value=value,
                child_value=comparator,
                file_path=file_path,
                prefix="Op",
                extra_field={"op": type(value.ops[ceil]).__name__, "index": ceil}
            )
            index += 0.5

    def _parse_left(self, value: ast.Compare, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.left,
            file_path=file_path,
            prefix="Left",
        )
        # It's a little bit complicated. First ops element, left and comparators are combined
        # So, if there is something like:
        # 1 < A < 2
        # then 1 and A are compared, then A and 2 are compared.
        self._save_relationship(
            parent_value=value,
            child_value=value.left,
            file_path=file_path,
            prefix="Op",
            extra_field={"op": type(value.ops[0]).__name__, "index": 0}
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.comparators[0],
            file_path=file_path,
            prefix="Op",
            extra_field={"op": type(value.ops[0]).__name__, "index": 0}
        )
