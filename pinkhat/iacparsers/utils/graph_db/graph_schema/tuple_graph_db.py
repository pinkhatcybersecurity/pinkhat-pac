import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import (
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.named_expr_graph_db import (
    NamedExprGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class TupleGraphDb(BaseGraphDb):
    TABLE_NAME = TableName.Tuple.value
    _rels = {
        "prefix": {
            "Dim": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
            ],
            "Elt": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.NamedExpr.value,
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

    def add(self, value: ast.Tuple, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            },
        )
        self._parse_dim(value, file_path)
        self._parse_elt(value, file_path)

    def _parse_elt(self, value: ast.Tuple, file_path: str):
        for elt in value.elts:
            if stmt := self._get_stmt(value=elt):
                stmt.add(elt, file_path=file_path)
        try:
            self._table.add_relation_group(
                stmt=self._stmt,
                parent_value=value,
                child_value=[elt for elt in value.elts],
                file_path=file_path,
                prefix="Elt",
                extra_field={},
            )
        except Exception as e:
            print(e)

    def _parse_dim(self, value: ast.Tuple, file_path: str):
        for dim in value.dims:
            if stmt := self._get_stmt(value=dim):
                stmt.add(dim, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[dim for dim in value.dims],
            file_path=file_path,
            prefix="Dim",
            extra_field={},
        )
