import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class DictGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.Dict.value
    _rels = {
        "prefix": {
            "Key": [
                TableName.Attribute.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Subscript.value,
            ],
            "Value": [
                TABLE_NAME,
                TableName.AnnAssign.value,
                TableName.Attribute.value,
                TableName.BinOp.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.JoinedStr.value,
                TableName.Lambda.value,
                TableName.List.value,
                TableName.ListComp.value,
                TableName.Name.value,
                TableName.Set.value,
                TableName.Subscript.value,
                TableName.Tuple.value,
                TableName.UnaryOp.value,
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

    def create_rel(self):
        for prefix, tables in self._rels.get("prefix", {}).items():
            self._table.create_relationship_group(
                to_table=tables,
                prefix=prefix,
                extra_fields=self._rels.get("extra_fields"),
            )

    def add(self, value: ast.Dict, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            },
        )
        [
            self._save_relationship(
                parent_value=value,
                child_value=key,
                file_path=file_path,
                prefix="Key",
            )
            for key in value.keys
        ]
        [
            self._save_relationship(
                parent_value=value,
                child_value=val,
                file_path=file_path,
                prefix="Value",
            )
            for val in value.values
        ]
