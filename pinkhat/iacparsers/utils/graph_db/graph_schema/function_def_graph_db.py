import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class FunctionDefGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.FunctionDef.value
    _rels = {
        "prefix": {
            "body": [
                TABLE_NAME,
                TableName.Assign.value,
                TableName.Expr.value,
                TableName.Return.value,
                TableName.Global.value,
                TableName.For.value,
                TableName.If.value,
                TableName.Try.value,
                TableName.ClassDef.value,
            ],
            "Decorator": [TableName.Call.value, TableName.Name.value],
            "Default": [
                TableName.arg.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Call.value,
            ],
            "KwDefault": [
                TableName.arg.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Call.value,
            ],
            "Args": [TableName.arg.value],
            "VarArg": [
                TableName.arg.value,
            ],
            "PosOnlyArg": [TableName.arg.value],
            "KwOnlyArg": [TableName.arg.value],
            "Kwarg": [TableName.arg.value],
            "TypeParam": [TableName.arg.value],
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
            Column(name="returns", column_type="STRING"),
            Column(name="type_comment", column_type="STRING"),
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

    def add(self, value: ast.FunctionDef, file_path: str):
        try:
            self._table.add(
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
        except Exception as e:
            print(e)
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
            self._table.add_relation(
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
                self._table.add_relation(
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
                self._table.add_relation(
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
            self._table.add_relation(
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
            if stmt := self._get_stmt(value=kw_default):
                stmt.add(value=kw_default, file_path=file_path)

        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[kw_default for kw_default in args.kw_defaults],
            file_path=file_path,
            prefix="KwDefault",
            extra_field={},
        )

    def _parse_defaults(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        for default in args.defaults:
            if stmt := self._get_stmt(value=default):
                stmt.add(value=default, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[default for default in args.defaults],
            file_path=file_path,
            prefix="Default",
            extra_field={},
        )

    def _parse_args(self, args: ast.arguments, file_path: str, value: ast.FunctionDef):
        for arg in args.args:
            stmt = self._get_stmt(value=arg)
            if arg:
                stmt.add(value=arg, file_path=file_path)
                self._table.add_relation(
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
                self._table.add_relation(
                    to_table=stmt.TABLE_NAME,
                    parent_value=value,
                    child_value=type_param,
                    file_path=file_path,
                    prefix="TypeParam",
                )

    def _parse_decorators(self, file_path: str, value: ast.FunctionDef):
        for decorator in value.decorator_list:
            if stmt := self._get_stmt(value=decorator):
                stmt.add(value=decorator, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[decorator for decorator in value.decorator_list],
            file_path=file_path,
            prefix="Decorator",
            extra_field={},
        )

    def _parse_body(self, file_path: str, value: ast.FunctionDef):
        for body in value.body:
            if stmt := self._get_stmt(body):
                stmt.add(value=body, file_path=file_path)
        self._table.add_relation_group(
            stmt=self._stmt,
            parent_value=value,
            child_value=[body for body in value.body],
            file_path=file_path,
            prefix="Body",
            extra_field={},
        )
