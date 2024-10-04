import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ClassDefGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.ClassDef.value
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS,
            "Decorator": [TableName.Attribute.value, TableName.Name.value],
            "Keyword": [TableName.keyword.value],
            "Base": [TableName.Attribute.value, TableName.Name.value],
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
            Column(name="name", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def create_rel(self):
        for prefix, tables in self._rels.get("prefix", {}).items():
            self._table.create_relationship_group(
                to_table=tables,
                prefix=prefix,
                extra_fields=self._rels.get("extra_fields"),
            )

    def add(self, value: ast.ClassDef, file_path: str):
        # TODO: More complicated, it requires many additional steps to validate functions
        self._table.save(
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
        self._parse_body(value=value, file_path=file_path)
        self._parse_base(value=value, file_path=file_path)
        self._parse_keyword(file_path=file_path, value=value)
        self._parse_type_params(file_path=file_path, value=value)

    def _parse_body(self, value: ast.ClassDef, file_path: str):
        for body in value.body:
            self._save_relationship(
                parent_value=value,
                child_value=body,
                file_path=file_path,
                prefix="Body",
            )

    def _parse_type_params(self, file_path: str, value: ast.ClassDef):
        for type_param in value.type_params:
            self._save_relationship(
                parent_value=value,
                child_value=type_param,
                file_path=file_path,
                prefix="TypeParam",
            )

    def _parse_keyword(self, value: ast.ClassDef, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=keyword,
                file_path=file_path,
                prefix="Keyword",
            )
            for keyword in value.keywords
        ]

    def _parse_decorators(self, file_path: str, value: ast.ClassDef):
        [
            self._save_relationship(
                parent_value=value,
                child_value=decorator,
                file_path=file_path,
                prefix="Decorator",
            )
            for decorator in value.decorator_list
        ]

    def _parse_base(self, value: ast.ClassDef, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=base,
                file_path=file_path,
                prefix="Base",
            )
            for base in value.bases
        ]
