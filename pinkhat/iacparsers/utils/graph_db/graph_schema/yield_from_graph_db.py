from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.yield_base_graph_db import YieldBaseGraphDb


class YieldFromGraphDb(YieldBaseGraphDb):
    """
    Yield from
    ```
    yield from spaghetti
    ```
    """
    TABLE_NAME: str = TableName.YieldFrom.value

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
