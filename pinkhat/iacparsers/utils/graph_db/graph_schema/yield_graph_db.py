from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.yield_base_graph_db import YieldBaseGraphDb


class YieldGraphDb(YieldBaseGraphDb):
    TABLE_NAME: str = TableName.Yield.value

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
