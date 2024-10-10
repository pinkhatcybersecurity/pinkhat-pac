from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.with_base_graph_db import (
    WithBaseGraphDb,
)


class AsyncWithGraphDb(WithBaseGraphDb):
    TABLE_NAME: str = TableName.AsyncWith.value

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
