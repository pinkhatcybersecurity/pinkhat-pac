import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class WithBaseGraphDb(BaseGraphDb):
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS,
            "Item": {
                "rels": [TableName.WithItem.value],
                "extra_fields": "index INT, lineno INT, file_path STRING",
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
            Column(name="type_comment", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.With | ast.AsyncWith, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "type_comment": value.type_comment,
                "file_path": file_path,
            }
        )
        self._parse_items(value=value, file_path=file_path)
        self._parse_body(value=value, file_path=file_path)

    def _parse_body(self, value: ast.With | ast.AsyncWith, file_path: str):
        [
            self._save_relationship(
                parent_value=value, child_value=body, file_path=file_path, prefix="Body"
            )
            for body in value.body
        ]

    def _parse_items(self, value: ast.With | ast.AsyncWith, file_path: str):
        index = -1
        [
            self._save_relationship(
                parent_value=value,
                child_value=item,
                file_path=file_path,
                prefix="Item",
                extra_field={"index": (index := index + 1)},
            )
            for item in value.items
        ]
