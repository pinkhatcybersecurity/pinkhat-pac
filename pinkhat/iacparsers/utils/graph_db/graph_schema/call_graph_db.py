import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.attribute_graph_db import AttributeGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.binop_graph_db import BinOpGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import ConstantGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.joinedstr_graph_db import JoinedStrGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.keyword_graph_db import KeywordGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.starred_graph_db import StarredGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class CallGraphDb(BaseGraphDb):
    TABLE_NAME = "Call"
    _rels = [
        {"to_table": NameGraphDb.TABLE_NAME, "prefix": "Func"},
        {
            "to_table": BinOpGraphDb.TABLE_NAME,
            "prefix": "Arg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Arg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": AttributeGraphDb.TABLE_NAME,
            "prefix": "Arg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Arg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": StarredGraphDb.TABLE_NAME,
            "prefix": "Arg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": KeywordGraphDb.TABLE_NAME,
            "prefix": "Keyword",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": AttributeGraphDb.TABLE_NAME,
            "prefix": "Func",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": JoinedStrGraphDb.TABLE_NAME,
            "prefix": "Arg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TABLE_NAME,
            "prefix": "Arg",
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

    def add(self, value: ast.Call, file_path: str):
        self._table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        stmt = self._get_stmt(value=value.func)
        if stmt:
            stmt.add(value=value.func, file_path=file_path)
            self._conn.execute(
                query=f"""
                    MATCH (u1:{self._table.name}), (u2:{type(value.func).__name__}) WHERE 
                    u1.lineno = $u1_lineno AND
                    u1.file_path = $file_path AND
                    u2.lineno = $u2_lineno AND
                    u2.file_path = $file_path
                    CREATE (u1)-[:Func_{type(value.func).__name__}_{self._table.name}_Rel]->(u2)
                    """,
                parameters={
                    "u1_lineno": value.lineno,
                    "u2_lineno": value.func.lineno,
                    "file_path": file_path,
                },
            )
        self._parse_args(file_path, value)
        self._parse_keywords(file_path, value)

    def _parse_keywords(self, file_path, value):
        for keyword in value.keywords:
            stmt = self._get_stmt(value=keyword)
            if stmt:
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=keyword,
                    file_path=file_path,
                    prefix="Keyword",
                )

    def _parse_args(self, file_path: str, value: ast.Call):
        for arg in value.args:
            stmt = self._get_stmt(value=arg)
            if stmt:
                stmt.add(value=arg, file_path=file_path)
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=arg,
                    file_path=file_path,
                    prefix="Arg",
                )
