from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.with_base_graph_db import (
    WithBaseGraphDb,
)


class WithGraphDb(WithBaseGraphDb):
    TABLE_NAME: str = TableName.With.value

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
