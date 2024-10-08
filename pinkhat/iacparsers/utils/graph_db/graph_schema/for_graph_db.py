import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema import AttributeGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.assign_graph_db import AssignGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.if_graph_db import IfGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.tuple_graph_db import TupleGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.expr_graph_db import ExprGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ForGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.For.value
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS,
            "Iter": [
                TableName.Attribute.value,
                TableName.BoolOp.value,
                TableName.Call.value,
                TableName.Name.value,
                TableName.Subscript.value,
            ],
            "Target": [TableName.Name.value, TableName.Tuple.value],
            "OrElse": [TableName.Expr.value],
        },
        "extra_fields": "lineno INT, file_path STRING",
    }

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
            Column(name="type_comment", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.For, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "type_comment": value.type_comment,
                "file_path": file_path,
            }
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.iter,
            file_path=file_path,
            prefix="Iter",
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.target,
            file_path=file_path,
            prefix="Target",
        )
        self._parse_body(value=value, file_path=file_path)
        self._parse_or_else(value=value, file_path=file_path)

    def _parse_or_else(self, value: ast.For, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=or_else,
                file_path=file_path,
                prefix="OrElse",
            )
            for or_else in value.orelse
        ]

    def _parse_body(self, value: ast.For, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=body,
                file_path=file_path,
                prefix="Body",
            )
            for body in value.body
        ]
