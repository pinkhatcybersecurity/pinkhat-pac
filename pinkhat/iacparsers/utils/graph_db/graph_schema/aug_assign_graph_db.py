import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.assign_base_graph_db import (
    AssignBaseGrapDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class AugAssignGraphDb(AssignBaseGrapDb):
    """
    Operations += i.e.
    ```
    item += 10
    ```
    """

    TABLE_NAME: str = TableName.AugAssign.value

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
            Column(name="op", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.AugAssign, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "op": type(value.op).__name__,
                "file_path": file_path,
            }
        )
        self._parse_target(value=value, file_path=file_path)
        self._parse_value(value=value, file_path=file_path)

    def _parse_target(self, value: ast.AugAssign, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.target,
            file_path=file_path,
            prefix="Target",
        )
