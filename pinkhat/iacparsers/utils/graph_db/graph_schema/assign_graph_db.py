import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.assign_base_graph_db import (
    AssignBaseGrapDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class AssignGraphDb(AssignBaseGrapDb):
    TABLE_NAME: str = TableName.Assign.value

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

    def add(self, value: ast.Assign, file_path: str):
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
        self._parse_targets(value=value, file_path=file_path)
        self._parse_value(value=value, file_path=file_path)

    def _parse_targets(self, value: ast.Assign, file_path: str):
        for target in value.targets:
            self._save_relationship(
                parent_value=value,
                child_value=target,
                file_path=file_path,
                prefix="Target",
            )
