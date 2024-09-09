import ast

from kuzu import Connection

from iacparsers.utils.graph_db.graph_schema.assign_graph_db import AssignGraphDb
from iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from iacparsers.utils.graph_db.graph_schema.class_def_graph_db import ClassDefGraphDb
from iacparsers.utils.graph_db.graph_schema.expr_graph_db import ExprGraphDb
from iacparsers.utils.graph_db.graph_schema.for_graph_db import ForGraphDb
from iacparsers.utils.graph_db.graph_schema.function_def_graph_db import (
    FunctionDefGraphDb,
)
from iacparsers.utils.graph_db.graph_schema.try_graph_db import TryGraphDb
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class ModuleGraphDb(BaseGraphDb):
    TABLE_NAME: str = "Module"
    _rels = [
        {
            "to_table": AssignGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ExprGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": FunctionDefGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ClassDefGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ForGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": TryGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._module_table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="name", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._module_table.create()

    def create_rel(self):
        for rel in self._rels:
            self._module_table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.Module, file_path: str):
        module_name = file_path.replace("/", ".")
        self._module_table.add(params={"name": module_name, "file_path": file_path})
        for body in value.body:
            stmt = self._get_stmt(body)
            if stmt:
                stmt.add(value=body, file_path=file_path)
                self._conn.execute(
                    query=f"""
                    MATCH (u1:{self._module_table.name}), (u2:{type(body).__name__}) WHERE 
                    u1.file_path = $file_path AND
                    u2.lineno = $lineno AND
                    u2.file_path = $file_path
                    CREATE (u1)-[:Body_{type(body).__name__}_{self._module_table.name}_Rel]->(u2)
                    """,
                    parameters={"file_path": file_path, "lineno": body.lineno},
                )
