import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class WithItemGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.WithItem.value
    _rels = {
        "prefix": {
            "ContextExpr": [TableName.Call.value, TableName.Name.value],
            "OptionalVar": [TableName.Name.value],
        },
        "extra_fields": "lineno INT, file_path STRING",
    }

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="file_path", column_type="STRING"),
        )

    def create_rel(self):
        for prefix, tables in self._rels.get("prefix", {}).items():
            self._table.create_relationship_group(
                to_table=tables,
                prefix=prefix,
                extra_fields=self._rels.get("extra_fields"),
            )

    def add(self, value: ast.withitem, file_path: str):
        self._table.save(
            params={
                "file_path": file_path,
            }
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.context_expr,
            file_path=file_path,
            prefix="ContextExpr",
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.optional_vars,
            file_path=file_path,
            prefix="OptionalVar",
        )
