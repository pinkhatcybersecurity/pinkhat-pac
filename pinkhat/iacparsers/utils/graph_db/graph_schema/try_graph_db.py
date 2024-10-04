import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class TryGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.Try.value
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS,
            "FinalBody": [
                TableName.Assign.value,
                TableName.Expr.value,
                TableName.If.value,
            ],
            "Handler": [TableName.ExceptHandler.value],
            "OrElse": [TableName.Expr.value],
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

    def add(self, value: ast.Try, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._parse_body(value=value, file_path=file_path)
        self._parse_handler(value=value, file_path=file_path)
        self._parse_final_body(value=value, file_path=file_path)
        self._parse_or_else(value=value, file_path=file_path)

    def _parse_or_else(self, value: ast.Try, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=or_else,
                file_path=file_path,
                prefix="OrElse",
            )
            for or_else in value.orelse
        ]

    def _parse_final_body(self, value: ast.Try, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=final,
                file_path=file_path,
                prefix="FinalBody",
            )
            for final in value.finalbody
        ]

    def _parse_handler(self, value: ast.Try, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=handler,
                file_path=file_path,
                prefix="Handler",
            )
            for handler in value.handlers
        ]

    def _parse_body(self, value: ast.Try, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=body,
                file_path=file_path,
                prefix="Body",
            )
            for body in value.body
        ]
