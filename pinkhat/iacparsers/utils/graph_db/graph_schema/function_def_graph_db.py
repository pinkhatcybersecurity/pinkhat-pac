import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.arg_graph_db import ArgGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.assign_graph_db import AssignGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import ConstantGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.expr_graph_db import ExprGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.global_graph_db import GlobalGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.return_graph_db import ReturnGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class FunctionDefGraphDb(BaseGraphDb):
    TABLE_NAME: str = "FunctionDef"
    _rels = [
        {
            "to_table": TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": AssignGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": CallGraphDb.TABLE_NAME,
            "prefix": "Decorator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "Args",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "VarArg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "PosOnlyArg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "KwOnlyArg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "Kwarg",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "KwDefault",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "Default",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ArgGraphDb.TABLE_NAME,
            "prefix": "TypeParam",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ExprGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ReturnGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": GlobalGraphDb.TABLE_NAME,
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": ConstantGraphDb.TABLE_NAME,
            "prefix": "Default",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": NameGraphDb.TABLE_NAME,
            "prefix": "Decorator",
            "extra_fields": "lineno INT, file_path STRING",
        },
        {
            "to_table": "ClassDef",
            "prefix": "Body",
            "extra_fields": "lineno INT, file_path STRING",
        },
    ]

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)
        self._function_def_table = Table(
            self.TABLE_NAME,
            self._conn,
            Column(name="p_id", column_type="SERIAL", primary_key=True),
            Column(name="col_offset", column_type="INT64"),
            Column(name="end_col_offset", column_type="INT64"),
            Column(name="end_lineno", column_type="INT64"),
            Column(name="lineno", column_type="INT"),
            Column(name="name", column_type="STRING"),
            Column(name="returns", column_type="STRING"),
            Column(name="type_comment", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def initialize(self, stmt: dict, expr: dict):
        self._stmt = stmt
        self._expr = expr
        self._function_def_table.create()

    def create_rel(self):
        for rel in self._rels:
            self._function_def_table.create_relationship(
                to_table=rel.get("to_table"),
                prefix=rel.get("prefix"),
                extra_fields=rel.get("extra_fields"),
            )

    def add(self, value: ast.FunctionDef, file_path: str):
        self._function_def_table.add(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "name": value.name,
                "returns": value.returns,
                "type_comment": value.type_comment,
                "file_path": file_path,
            },
        )
        self._parse_body(value=value, file_path=file_path)
        self._parse_decorators(file_path=file_path, value=value)
        self._parse_type_params(file_path=file_path, value=value)
        self._parse_arguments(file_path, value)

    def _parse_arguments(self, file_path: str, value: ast.FunctionDef):
        args: ast.arguments = value.args
        self._parse_args(args=args, file_path=file_path, value=value)
        self._parse_defaults(args=args, file_path=file_path, value=value)
        self._parse_kw_defaults(args=args, file_path=file_path, value=value)
        self._parse_kwarg(args=args, file_path=file_path, value=value)
        self._parse_kw_only_args(args=args, file_path=file_path, value=value)
        self._parse_posonlyargs(args=args, file_path=file_path, value=value)
        self._parse_vararg(args=args, file_path=file_path, value=value)

    def _parse_vararg(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        vararg = args.vararg
        stmt = self._get_stmt(value=vararg)
        if stmt:
            stmt.add(value=vararg, file_path=file_path)
            self._function_def_table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=vararg,
                file_path=file_path,
                prefix="VarArg",
            )

    def _parse_posonlyargs(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        for posonlyarg in args.posonlyargs:
            stmt = self._get_stmt(value=posonlyarg)
            if stmt:
                stmt.add(value=posonlyarg, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=posonlyarg,
                    file_path=file_path,
                    prefix="PosOnlyArg",
                )

    def _parse_kw_only_args(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        for kwonlyarg in args.kwonlyargs:
            stmt = self._get_stmt(value=kwonlyarg)
            if stmt:
                stmt.add(value=kwonlyarg, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=kwonlyarg,
                    file_path=file_path,
                    prefix="KwOnlyArg",
                )

    def _parse_kwarg(self, args: ast.arguments, file_path: str, value: ast.FunctionDef):
        kwarg = args.kwarg
        stmt = self._get_stmt(value=kwarg)
        if stmt:
            stmt.add(value=kwarg, file_path=file_path)
            self._function_def_table.add_relation(
                to_table=stmt.TABLE_NAME,
                parent_value=value,
                child_value=kwarg,
                file_path=file_path,
                prefix="Kwarg",
            )

    def _parse_kw_defaults(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        for kw_default in args.kw_defaults:
            stmt = self._get_stmt(value=kw_default)
            if stmt:
                stmt.add(value=kw_default, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=kw_default,
                    file_path=file_path,
                    prefix="KwDefault",
                )

    def _parse_defaults(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        for default in args.defaults:
            stmt = self._get_stmt(value=default)
            if stmt:
                stmt.add(value=default, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=default,
                    file_path=file_path,
                    prefix="Default",
                )

    def _parse_args(self, args: ast.arguments, file_path: str, value: ast.FunctionDef):
        for arg in args.args:
            stmt = self._get_stmt(value=arg)
            if arg:
                stmt.add(value=arg, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=arg,
                    file_path=file_path,
                    prefix="Args",
                )

    def _parse_type_params(self, file_path: str, value: ast.FunctionDef):
        for type_param in value.type_params:
            stmt = self._get_stmt(value=type_param)
            if stmt:
                stmt.add(value=type_param, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=type_param,
                    file_path=file_path,
                    prefix="TypeParam",
                )

    def _parse_decorators(self, file_path: str, value: ast.FunctionDef):
        for decorator in value.decorator_list:
            stmt = self._get_stmt(value=decorator)
            if stmt:
                stmt.add(value=decorator, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=decorator,
                    file_path=file_path,
                    prefix="Decorator",
                )

    def _parse_body(self, file_path: str, value: ast.FunctionDef):
        for body in value.body:
            stmt = self._get_stmt(body)
            if stmt:
                stmt.add(value=body, file_path=file_path)
                self._function_def_table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=body,
                    file_path=file_path,
                    prefix="Body",
                )
