import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class AnnAssignGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.AnnAssign.value
    _rels = {
        "prefix": {
            "Annotation": [
                TABLE_NAME,
                TableName.Attribute.value,
                TableName.BinOp.value,
                TableName.Call.value,
                TableName.Name.value,
                TableName.Subscript.value,
            ],
            "Target": [TableName.Attribute.value, TableName.Name.value],
            "Value": [
                TableName.Attribute.value,
                TableName.Await.value,
                TableName.BoolOp.value,
                TableName.BinOp.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Dict.value,
                TableName.List.value,
                TableName.ListComp.value,
                TableName.Name.value,
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
            Column(name="simple", column_type="INT"),
            Column(name="file_path", column_type="STRING"),
        )

    def create_rel(self):
        for prefix, tables in self._rels.get("prefix", {}).items():
            self._table.create_relationship_group(
                to_table=tables,
                prefix=prefix,
                extra_fields=self._rels.get("extra_fields"),
            )

    def add(self, value: ast.AnnAssign, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "simple": value.simple,
                "file_path": file_path,
            }
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.target,
            file_path=file_path,
            prefix="Target",
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.value,
            file_path=file_path,
            prefix="Value",
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.annotation,
            file_path=file_path,
            prefix="Annotation",
        )
