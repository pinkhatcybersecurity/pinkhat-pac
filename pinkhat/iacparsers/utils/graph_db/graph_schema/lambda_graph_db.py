import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.body_relationships import (
    BODY_RELATIONSHIPS,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class LambdaGraphDb(BaseGraphDb):
    TABLE_NAME: str = TableName.Lambda.value
    _rels = {
        "prefix": {
            "Body": BODY_RELATIONSHIPS
            + [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Constant.value,
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

    def add(self, value: ast.Lambda, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            },
        )
        self._parse_body(value=value, file_path=file_path)
        self._parse_arguments(value=value, file_path=file_path)

    def _parse_arguments(self, value: ast.Lambda, file_path: str):
        args: ast.arguments = value.args
        self._parse_args(value=value, args=args, file_path=file_path)
        self._parse_defaults(value=value, args=args, file_path=file_path)
        self._parse_kw_defaults(value=value, args=args, file_path=file_path)
        self._parse_kwarg(value=value, args=args, file_path=file_path)
        self._parse_kw_only_args(value=value, args=args, file_path=file_path)
        self._parse_posonlyargs(value=value, args=args, file_path=file_path)
        self._parse_vararg(value=value, args=args, file_path=file_path)

    def _parse_vararg(self, value: ast.Lambda, args: ast.arguments, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=args.vararg,
            file_path=file_path,
            prefix="VarArg",
        )

    def _parse_posonlyargs(
        self, value: ast.Lambda, args: ast.arguments, file_path: str
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
        self, value: ast.Lambda, args: ast.arguments, file_path: str
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

    def _parse_kwarg(self, value: ast.Lambda, args: ast.arguments, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=args.kwarg,
            file_path=file_path,
            prefix="Kwarg",
        )

    def _parse_kw_defaults(
        self, value: ast.Lambda, args: ast.arguments, file_path: str
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

    def _parse_defaults(self, value: ast.Lambda, args: ast.arguments, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=default,
                file_path=file_path,
                prefix="Default",
            )
            for default in args.defaults
        ]

    def _parse_args(self, value: ast.Lambda, args: ast.arguments, file_path: str):
        [
            self._save_relationship(
                parent_value=value,
                child_value=arg,
                file_path=file_path,
                prefix="Arg",
            )
            for arg in args.args
        ]

    def _parse_body(self, value: ast.Lambda, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.body,
            file_path=file_path,
            prefix="Body",
        )
