import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName


class AssignBaseGrapDb(BaseGraphDb):
    _rels = {
        "prefix": {
            "Value": [
                TableName.Attribute.value,
                TableName.Await.value,
                TableName.BinOp.value,
                TableName.BoolOp.value,
                TableName.Call.value,
                TableName.Compare.value,
                TableName.Constant.value,
                TableName.Dict.value,
                TableName.DictComp.value,
                TableName.GeneratorExp.value,
                TableName.IfExp.value,
                TableName.JoinedStr.value,
                TableName.Lambda.value,
                TableName.List.value,
                TableName.ListComp.value,
                TableName.Name.value,
                TableName.Tuple.value,
                TableName.Set.value,
                TableName.SetComp.value,
                TableName.Subscript.value,
            ],
            "Target": [
                TableName.Attribute.value,
                TableName.Name.value,
                TableName.Tuple.value,
                TableName.Subscript.value,
            ],
        },
        "extra_fields": "lineno INT, file_path STRING",
    }

    def __init__(self, conn: Connection):
        super().__init__(conn=conn)

    def _parse_value(self, value: ast.Assign | ast.AugAssign, file_path: str):
        self._save_relationship(
            parent_value=value,
            child_value=value.value,
            file_path=file_path,
            prefix="Value",
        )
