import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.attribute_graph_db import (
    AttributeGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.binop_graph_db import BinOpGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import (
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.list_comp_graph_db import (
    ListCompGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.tuple_graph_db import TupleGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class AssignGraphDb(BaseGraphDb):
    TABLE_NAME = "Assign"
    _rels = [
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Target",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": BinOpGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TupleGraphDb.TABLE_NAME,
            "prefix": "Target",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TupleGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": AttributeGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": AttributeGraphDb.TABLE_NAME,
            "prefix": "Target",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ListCompGraphDb.TABLE_NAME,
            "prefix": "Value",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._assign_table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="col_offset", column_type="INT64"),
            Column(name="end_col_offset", column_type="INT64"),
            Column(name="end_lineno", column_type="INT64"),
            Column(name="lineno", column_type="INT"),
            Column(name="type_comment", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._assign_table.create()

    def create_rel(self):
        for rel in self._rels:
            self._assign_table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.Assign, file_path: str):
        self._assign_table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "type_comment": value.type_comment,
                "file_path": file_path,
            }
        )
        for target in value.targets:
            stmt = self._get_stmt(target)
            if stmt:
                stmt.add(value=target, file_path=file_path)
                self._assign_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=target,
                    file_path=file_path,
                    prefix="Target",
                )
        stmt = self._get_stmt(value.value)
        if stmt:
            stmt.add(value=value.value, file_path=file_path)
            self._assign_table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=value.value,
                file_path=file_path,
                prefix="Value",
            )
