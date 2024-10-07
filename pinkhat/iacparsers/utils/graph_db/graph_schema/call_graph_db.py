import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class CallGraphDb(BaseGraphDb):
    TABLE_NAME = TableName.Call.value
    _rels = {
        "prefix": {
            "Arg": [
                TABLE_NAME,
                TableName.Attribute.value,
                TableName.Await.value,
                TableName.BinOp.value,
                TableName.BoolOp.value,
                TableName.Compare.value,
                TableName.Constant.value,
                TableName.Dict.value,
                TableName.JoinedStr.value,
                TableName.List.value,
                TableName.Name.value,
                TableName.Starred.value,
                TableName.Subscript.value,
                TableName.Tuple.value,
                TableName.UnaryOp.value,
            ],
            "Keyword": [TableName.keyword.value],
            "Func": [
                TABLE_NAME,
                TableName.Attribute.value,
                TableName.Name.value,
                TableName.Subscript.value,
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

    def add(self, value: ast.Call, file_path: str):
        self._table.save(
            params={
                "col_offset": value.col_offset,
                "end_col_offset": value.end_col_offset,
                "end_lineno": value.end_lineno,
                "lineno": value.lineno,
                "file_path": file_path,
            }
        )
        self._save_relationship(
            parent_value=value,
            child_value=value.func,
            file_path=file_path,
            prefix="Func",
        )
        # # self._conn.execute(
        # #     query=f"""
        # #         MATCH (u1:{self._table.name}), (u2:{type(value.func).__name__}) WHERE
        # #         u1.lineno = $u1_lineno AND
        # #         u1.file_path = $file_path AND
        # #         u2.lineno = $u2_lineno AND
        # #         u2.file_path = $file_path
        # #         CREATE (u1)-[:Func_{type(value.func).__name__}_{self._table.name}_Rel]->(u2)
        # #         """,
        # #     parameters={
        # #         "u1_lineno": value.lineno,
        # #         "u2_lineno": value.func.lineno,
        # #         "file_path": file_path,
        # #     },
        # # )
        self._parse_args(file_path=file_path, value=value)
        self._parse_keywords(file_path=file_path, value=value)

    def _parse_keywords(self, file_path, value):
        for keyword in value.keywords:
            self._save_relationship(
                parent_value=value,
                child_value=keyword,
                file_path=file_path,
                prefix="Keyword",
            )

    def _parse_args(self, file_path: str, value: ast.Call):
        for arg in value.args:
            self._save_relationship(
                parent_value=value,
                child_value=arg,
                file_path=file_path,
                prefix="Arg",
            )
