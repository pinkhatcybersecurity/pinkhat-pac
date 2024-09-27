import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class IfGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.If.value
    _rels = {
        "prefix": {
            "Body": [
                TableName.Assign.value,
                TableName.Expr.value,
                TableName.For.value,
                TableName.FunctionDef.value,
                TableName.Try.value,
                TableName.Raise.value,
                TableName.Return.value,
                TABLE_NAME,
            ],
            "If": [
                TableName.Attribute.value,
                TableName.BoolOp.value,
                TableName.Call.value,
                TableName.Compare.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
            ],
            "OrElse": [
                TableName.Assign.value,
                TableName.Attribute.value,
                TableName.Expr.value,
                TableName.For.value,
                TableName.Raise.value,
                TableName.Return.value,
                TABLE_NAME,
            ],
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
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict):
        self._stmt = stmt
        self._table.create()

    def create_rel(self):
        for prefix, tables in self._rels.get("prefix", {}).items():
            self._table.create_relationship_group(
                to_table=tables,
                prefix=prefix,
                extra_fields=self._rels.get("extra_fields"),
            )

    def add(self, value: ast.If, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._parse_test(value=value, file_path=file_path)
        self._parse_body(value=value, file_path=file_path)
        or_else: ast.If
        for or_else in value.orelse:
            if stmt := self._get_stmt(value=or_else):
                stmt.add(value=or_else, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[or_else for or_else in value.orelse],
            file_path=file_path,
            prefix="OrElse",
            extra_field={},
        )

    def _parse_body(self, value: ast.If, file_path: str):
        for body in value.body:
            if stmt := self._get_stmt(value=body):
                stmt.add(value=body, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[body for body in value.body],
            file_path=file_path,
            prefix="Body",
            extra_field={},
        )

    def _parse_test(self, value: ast.If, file_path: str):
        if stmt := self._get_stmt(value=value.test):
            stmt.add(value=value.test, file_path=file_path)
            try:
                self._table.add_relation_group(
                    stmt=self._stmt,
                    parent_value=value,
                    child_value=[value.test],
                    file_path=file_path,
                    prefix="If",
                    extra_field={},
                )
            except Exception as e:
                print(e)
