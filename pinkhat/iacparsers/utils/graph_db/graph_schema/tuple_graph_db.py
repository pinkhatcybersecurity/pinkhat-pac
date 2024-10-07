import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class TupleGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.Tuple.value
    _rels = {
        "prefix": {
            "Dim": [
                TableName.Attribute.value,
                TableName.BoolOp.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Dict.value,
                TableName.List.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
                TableName.Subscript.value,
            ],
            "Elt": [
                TableName.Attribute.value,
                TableName.BoolOp.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Dict.value,
                TableName.List.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
                TableName.Tuple.value,
                TableName.Subscript.value,
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

    def add(self, value: ast.Tuple, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            },
        )
        self._parse_dim(value, file_path)
        self._parse_elt(value, file_path)

    def _parse_elt(self, value: ast.Tuple, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=elt,
                file_path=file_path,
                prefix="Elt",
            )
            for elt in value.elts
        ]

    def _parse_dim(self, value: ast.Tuple, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=dim,
                file_path=file_path,
                prefix="Dim",
            )
            for dim in value.dims
        ]
