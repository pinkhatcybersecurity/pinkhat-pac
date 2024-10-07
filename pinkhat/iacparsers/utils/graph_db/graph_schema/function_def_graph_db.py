import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class FunctionDefGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.FunctionDef.value
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS,
            "Returns": [
                TableName.Attribute.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Tuple.value,
                TableName.Subscript.value,
            ],
            "Decorator": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Name.value,
            ],
            "Default": [
                TableName.arg.value,
                TableName.Constant.value,
                TableName.Dict.value,
                TableName.Name.value,
                TableName.Call.value,
            ],
            "KwDefault": [
                TableName.arg.value,
                TableName.Call.value,
                TableName.Constant.value,
                TableName.Name.value,
                TableName.Tuple.value,
            ],
            "Arg": [TableName.arg.value],
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
            Column(name="type_comment", column_type="STRING"),
            Column(name="file_path", column_type="STRING"),
        )

    def add(self, value: ast.FunctionDef, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "name": value.name,
                "type_comment": value.type_comment,
                "file_path": file_path,
            },
        )
        self._parse_body(value=value, file_path=file_path)
        self._parse_returns(value=value, file_path=file_path)
        self._parse_decorators(file_path=file_path, value=value)
        self._parse_type_params(file_path=file_path, value=value)
        self._parse_arguments(file_path, value)

    def _parse_returns(self, value: ast.FunctionDef, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.returns,
            file_path=file_path,
            prefix="Returns",
        )

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
        self._save_relationship(
            parent_value=value,
            child_value=args.vararg,
            file_path=file_path,
            prefix="VarArg",
        )

    def _parse_posonlyargs(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        [
            self._save_relationship(
                parent_value=value,
                child_value=posonlyarg,
                file_path=file_path,
                prefix="PosOnlyArg",
            )
            for posonlyarg in args.posonlyargs
        ]

    def _parse_kw_only_args(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        [
            self._save_relationship(
                parent_value=value,
                child_value=kwonlyarg,
                file_path=file_path,
                prefix="KwOnlyArg",
            )
            for kwonlyarg in args.kwonlyargs
        ]

    def _parse_kwarg(self, args: ast.arguments, file_path: str, value: ast.FunctionDef):
        self._save_relationship(
            parent_value=value,
            child_value=args.kwarg,
            file_path=file_path,
            prefix="Kwarg",
        )

    def _parse_kw_defaults(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        [
            self._save_relationship(
                parent_value=value,
                child_value=kw_default,
                file_path=file_path,
                prefix="KwDefault",
            )
            for kw_default in args.kw_defaults
        ]

    def _parse_defaults(
        self, args: ast.arguments, file_path: str, value: ast.FunctionDef
    ):
        [
            self._save_relationship(
                parent_value=value,
                child_value=default,
                file_path=file_path,
                prefix="Default",
            )
            for default in args.defaults
        ]

    def _parse_args(self, args: ast.arguments, file_path: str, value: ast.FunctionDef):
        [
            self._save_relationship(
                parent_value=value,
                child_value=arg,
                file_path=file_path,
                prefix="Arg",
            )
            for arg in args.args
        ]

    def _parse_type_params(self, file_path: str, value: ast.FunctionDef):
        [
            self._save_relationship(
                parent_value=value,
                child_value=type_param,
                file_path=file_path,
                prefix="TypeParam",
            )
            for type_param in value.type_params
        ]

    def _parse_decorators(self, file_path: str, value: ast.FunctionDef):
        [
            self._save_relationship(
                parent_value=value,
                child_value=decorator,
                file_path=file_path,
                prefix="Decorator",
            )
            for decorator in value.decorator_list
        ]

    def _parse_body(self, file_path: str, value: ast.FunctionDef):
        [
            self._save_relationship(
                parent_value=value,
                child_value=body,
                file_path=file_path,
                prefix="Body",
            )
            for body in value.body
        ]
