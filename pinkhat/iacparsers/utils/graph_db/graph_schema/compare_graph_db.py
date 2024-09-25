import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.tuple_graph_db import TupleGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import (
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.list_graph_db import ListGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.named_expr_graph_db import (
    NamedExprGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class CompareGraphDb(BaseGraphDb):
    TABLE_NAME: str = "Compare"
    _rels = [
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Comparator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ListGraphDb.TABLE_NAME,
            "prefix": "Comparator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Comparator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NamedExprGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TupleGraphDb.TABLE_NAME,
            "prefix": "Left",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TupleGraphDb.TABLE_NAME,
            "prefix": "Comparator",
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
        self._table.create_relationship_group(
            to_table=[
                ConstantGraphDb.TABLE_NAME,
                NameGraphDb.TABLE_NAME,
                TupleGraphDb.TABLE_NAME,
                ListGraphDb.TABLE_NAME,
                NamedExprGraphDb.TABLE_NAME,
            ],
            prefix="Op",
            extra_fields="index INT, lineno INT, op STRING, file_path STRING",
        )

    def add(self, value: ast.Compare, file_path: str):
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
            parent_value=value,
            child_value=value.left,
            file_path=file_path,
            prefix="Left",
        )
        for comparator in value.comparators:
            self._add_relationship(
                parent_value=value,
                child_value=comparator,
                file_path=file_path,
                prefix="Comparator",
            )
        index = 0
        expressions = {}
        expressions.update(self._stmt)
        expressions.update(self._expr)
        # It's a little bit complicated. First ops element, left and comparators are combined
        self._table.add_relation_group(
            stmt=expressions,
            parent_value=value,
            child_value=[value.left, value.comparators[0]],
            file_path=file_path,
            prefix="Op",
            extra_field={"op": type(value.ops[0]).__name__, "index": index},
        )
        index += 1
        # Collect the rest of the elements. Go through the list - 1.
        # The last element is not assigned to anything. So, it can be skipped.
        for ind in range(len(value.comparators) - 1):
            self._table.add_relation_group(
                stmt=expressions,
                parent_value=value,
                child_value=[value.comparators[ind], value.comparators[ind + 1]],
                file_path=file_path,
                prefix="Op",
                extra_field={"op": type(value.ops[ind + 1]).__name__, "index": index},
            )
            index += 1
