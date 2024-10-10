import ast

from kuzu import Connection

from pinkhat.iacparsers.utils.graph_db.graph_schema.base_graph_db import BaseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column
from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_table import Table


class SetCompGraphDb(BaseGraphDb):
    """
    Set creation using comprehension
    ```
    healthy_fruits = {fruit for fruit in fruits if fruit}
    ```
    """

    TABLE_NAME = TableName.SetComp.value
    _rels = {
        "prefix": {
            "Elt": [
                TableName.Attribute.value,
                TableName.Call.value,
                TableName.Name.value,
            ],
            "Generator": [TableName.comprehension.value],
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

    def add(self, value: ast.SetComp, file_path: str):
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
            child_value=value.elt,
            file_path=file_path,
            prefix="Elt",
        )
        for generator in value.generators:
            self._save_relationship(
                parent_value=value,
                child_value=generator,
                file_path=file_path,
                prefix="Generator",
            )
