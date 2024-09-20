import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.function_def_graph_db import (
    FunctionDefGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ClassDefGraphDb(BaseGraphDb):
    TABLE_NAME: str = "ClassDef"
    _rels = [
        {
            "to_table": FunctionDefGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Decorator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Base",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._class_table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="col_offset", column_type="INT64"),
            Column(name="end_col_offset", column_type="INT64"),
            Column(name="end_lineno", column_type="INT64"),
            Column(name="lineno", column_type="INT"),
            Column(name="name", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._class_table.create()

    def create_rel(self):
        for rel in self._rels:
            self._class_table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.ClassDef, file_path: str):
        # TODO: More complicated, it requires many additional steps to validate functions
        self._class_table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "name": value.name,
                "file_path": file_path,
            }
        )
        self._parse_decorators(file_path=file_path, value=value)
        self._parse_body(file_path=file_path, value=value)
        self._parse_base(file_path=file_path, value=value)
        self._parse_keyword(file_path=file_path, value=value)
        self._parse_type_params(file_path=file_path, value=value)

    def _parse_body(self, file_path: str, value: ast.ClassDef):
        for body in value.body:
            stmt = self._get_stmt(body)
            if stmt:
                stmt.add(value=body, file_path=file_path)
                self._class_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=body,
                    file_path=file_path,
                    prefix="Body",
                )

    def _parse_type_params(self, file_path: str, value: ast.ClassDef):
        for type_param in value.type_params:
            stmt = self._get_stmt(value=type_param)
            if stmt:
                stmt.add(value=type_param, file_path=file_path)
                self._class_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=type_param,
                    file_path=file_path,
                    prefix="TypeParam",
                )

    def _parse_keyword(self, file_path: str, value: ast.ClassDef):
        for keyword in value.keywords:
            stmt = self._get_stmt(value=keyword)
            if stmt:
                stmt.add(value=keyword, file_path=file_path)
                self._class_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=keyword,
                    file_path=file_path,
                    prefix="Keyword",
                )

    def _parse_decorators(self, file_path: str, value: ast.ClassDef):
        for decorator in value.decorator_list:
            stmt = self._get_stmt(decorator)
            if stmt:
                stmt.add(value=decorator, file_path=file_path)
                self._class_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=decorator,
                    file_path=file_path,
                    prefix="Decorator",
                )

    def _parse_base(self, file_path: str, value: ast.ClassDef):
        for base in value.bases:
            stmt = self._get_stmt(base)
            if stmt:
                stmt.add(value=base, file_path=file_path)
                self._class_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=base,
                    file_path=file_path,
                    prefix="Base",
                )
