import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ComprehensionGraphDb(BaseGraphDb):
    TABLE_NAME: str = "Comprehension"
    _rels = {
        "prefix": {
            "Iter": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Name.value,
                TableName.Subscript.value,
            ],
            "Target": [TableName.Name.value, TableName.Tuple.value],
            "If": [TableName.Call.value, TableName.Compare.value],
        },
        "extra_fields": "lineno INT, file_path STRING",
    }

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="is_async", column_type="INT"),
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.comprehension, file_path: str):
        self._table.save(
            params={
                "is_async": value.is_async,
                "file_path": file_path,
            }
        )
        [
            self._save_relationship(
                parent_value=value,
                child_value=if_stmt,
                file_path=file_path,
                prefix="If",
            )
            for if_stmt in value.ifs
        ]
        self._save_relationship(
            parent_value=value,
            child_value=value.iter,
            file_path=file_path,
            prefix="Iter",
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.target,
            file_path=file_path,
            prefix="Target",
        )
