import ast
from abc import ABC, abstractmethod

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class IfBaseGraphDb(ABC, BaseGraphDb):
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS,
            "Test": [
                TableName.Attribute.value,
                TableName.BoolOp.value,
                TableName.Call.value,
                TableName.Compare.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
                TableName.UnaryOp.value,
            ],
            "OrElse": BODY_RELATIONSHIPS,
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

    def add(self, value: ast.If | ast.IfExp, file_path: str):
        self._table.save(
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
        self._parse_or_else(value=value, file_path=file_path)

    @abstractmethod
    def _parse_body(self, value: ast.If | ast.IfExp, file_path: str):
        pass

    @abstractmethod
    def _parse_or_else(self, value: ast.If | ast.IfExp, file_path: str):
        pass

    def _parse_test(self, value: ast.If | ast.IfExp, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.test,
            file_path=file_path,
            prefix="Test",
        )
