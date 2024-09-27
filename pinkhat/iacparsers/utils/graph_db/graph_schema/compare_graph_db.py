import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
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
            ],
            "Comparator": [
                TableName.Attribute.value,
                TableName.Constant.value,
                TableName.List.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
                TableName.Tuple.value,
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
        self._table.create_relationship_group(
            to_table=[
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Tuple.value,
                TableName.List.value,
                TableName.NamedExpr.value,
                TableName.Attribute.value,
                TableName.Call.value,
            ],
            prefix="Op",
            extra_fields="index INT, lineno INT, op STRING, file_path STRING",
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
        self._parse_comparator(value=value, file_path=file_path)
        index = 0
        # It's a little bit complicated. First ops element, left and comparators are combined
        try:
            self._table.add_relation_group(
                stmt=self._stmt,
                parent_value=value,
                child_value=[value.left, value.comparators[0]],
                file_path=file_path,
                prefix="Op",
                extra_field={"op": type(value.ops[0]).__name__, "index": index},
            )
        except Exception as e:
            print(e)
        index += 1
        # Collect the rest of the elements. Go through the list - 1.
        # The last element is not assigned to anything. So, it can be skipped.
        for ind in range(len(value.comparators) - 1):
            self._table.add_relation_group(
                stmt=self._stmt,
                parent_value=value,
                child_value=[value.comparators[ind], value.comparators[ind + 1]],
                file_path=file_path,
                prefix="Op",
                extra_field={"op": type(value.ops[ind + 1]).__name__, "index": index},
            )
            index += 1

    def _parse_comparator(self, value: ast.Compare, file_path: str):
        for comparator in value.comparators:
            if stmt := self._get_stmt(value=comparator):
                stmt.add(value=comparator, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[comparator for comparator in value.comparators],
            file_path=file_path,
            prefix="Comparator",
            extra_field={},
        )

    def _parse_left(self, value: ast.Compare, file_path: str):
        if stmt := self._get_stmt(value=value.left):
            stmt.add(value.left, file_path=file_path)
        try:
            self._table.add_relation_group(
                stmt=self._stmt,
                parent_value=value,
                child_value=[value.left],
                file_path=file_path,
                prefix="Left",
                extra_field={},
            )
        except Exception as e:
            print(e)
