import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.comprehension_graph_db import (
    ComprehensionGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.list_graph_db import ListGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ListCompGraphDb(BaseGraphDb):
    TABLE_NAME = "ListComp"
    _rels = [
        {
            "to_table": ListGraphDb.TABLE_NAME,
            "prefix": "Elt",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ComprehensionGraphDb.TABLE_NAME,
            "prefix": "Generator",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

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
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._table.create()

    def create_rel(self):
        for rel in self._rels:
            self._table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.ListComp, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._add_relationship(
            parent_value=value, child_value=value.elt, file_path=file_path, prefix="Elt"
        )
        for generator in value.generators:
            self._add_relationship(
                parent_value=value,
                child_value=generator,
                file_path=file_path,
                prefix="Generator",
            )
