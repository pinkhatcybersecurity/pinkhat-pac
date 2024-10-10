import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.if_base_graph_db import (
    IfBaseGraphDb,
)


class IfExpGraphDb(IfBaseGraphDb):
    """
    Inline if representation:
    ```
    size = "big" if self._big else "small"
    ```
    """

    TABLE_NAME: str = TableName.IfExp.value

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)

    def _parse_body(self, value: ast.IfExp, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.body,
            file_path=file_path,
            prefix="Body",
        )

    def _parse_or_else(self, value: ast.IfExp, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.orelse,
            file_path=file_path,
            prefix="OrElse",
        )
