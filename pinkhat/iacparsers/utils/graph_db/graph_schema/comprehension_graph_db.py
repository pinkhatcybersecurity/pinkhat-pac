import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import CallGraphDb, NameGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table
from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb


class ComprehensionGraphDb(BaseGraphDb):
    TABLE_NAME = "Comprehension"
    _rels = [
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Iter",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Target",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="is_async", column_type="INT"),
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

    def add(self, value: ast.comprehension, file_path: str):
        self._table.add(
            params={
                "is_async": value.is_async,
                "file_path": file_path,
            }
        )
        for if_stmt in value.ifs:
            self._add_relationship(
                parent_value=value,
                child_value=if_stmt,
                file_path=file_path,
                prefix="If",
            )
        self._add_relationship(
            parent_value=value,
            child_value=value.iter,
            file_path=file_path,
            prefix="Iter",
        )
        self._add_relationship(
            parent_value=value,
            child_value=value.target,
            file_path=file_path,
            prefix="Target",
        )
