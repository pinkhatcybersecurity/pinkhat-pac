import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class NotEqGraphDb(BaseGraphDb):
    TABLE_NAME: str = "NotEq"

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict):
        self._stmt = stmt
        self._table.create()

    def add(self, value: ast.NotEq, file_path: str):
        self._table.save(
            params={
                "file_path": file_path,
            }
        )
