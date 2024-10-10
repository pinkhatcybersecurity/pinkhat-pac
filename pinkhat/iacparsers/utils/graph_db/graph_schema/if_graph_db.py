import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.if_base_graph_db import (
    IfBaseGraphDb,
)


class IfGraphDb(IfBaseGraphDb):
    TABLE_NAME: str = TableName.If.value

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)

    def _parse_body(self, value: ast.If, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=body,
                file_path=file_path,
                prefix="Body",
            )
            for body in value.body
        ]

    def _parse_or_else(self, value: ast.If, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=or_else,
                file_path=file_path,
                prefix="OrElse",
            )
            for or_else in value.orelse
        ]
