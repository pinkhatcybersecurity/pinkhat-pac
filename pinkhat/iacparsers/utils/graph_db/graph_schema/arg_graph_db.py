import ast
from venv import logger

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ArgGraphDb(BaseGraphDb):
    TABLE_NAME = "Arg"

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
            Column(name="annotation", column_type="STRING"),
            Column(name="arg", column_type="STRING"),
            Column(name="type_comment", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.arg, file_path: str):
        self._table.save(
            params={
                # "annotation": value.annotation,
                "arg": value.arg,
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "type_comment": value.type_comment,
                "file_path": file_path,
            }
        )
        logger.warning("Don't forget about support annotations")
