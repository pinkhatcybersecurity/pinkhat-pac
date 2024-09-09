import re

from kuzu import Connection
from loguru import logger

from iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column


class Table:
    def __init__(self, name: str, conn: Connection, *args):
        self._name = name
        self._conn = conn
        self._columns = args
        self._type_validation()

    @property
    def name(self):
        return self._name

    def _type_validation(self):
        if not re.search(r"^[A-Za-z0-9_]*$", self._name):
            self._raise_error(error=f"The table name is not alpha {self._name}")
        for column in self._columns:
            if not re.search(r"^[A-Za-z0-9_]*$", column.name):
                self._raise_error(error=f"The column name is not alpha {column.name}")
            if not re.search(r"^[A-Za-z0-9_]*$", column.column_type):
                self._raise_error(
                    error=f"The column type is not alpha {column.column_type}"
                )

    def create(self):
        primary_key = ""
        stmt = ""
        column: Column
        for column in self._columns:
            if column.primary_key:
                primary_key = f"PRIMARY KEY ({column.name})"
            stmt = f"{stmt if stmt else ''}{column.name} {column.column_type},"
        self._conn.execute(f"CREATE NODE TABLE {self._name}({stmt}{primary_key})")

    def create_relationship(self, to_table: str, prefix: str, extra_fields: str = None):
        if not re.search(r"^[A-Za-z0-9_]*$", to_table):
            self._raise_error(error=f"The table name is not alpha {to_table}")
        self._conn.execute(
            f"CREATE REL TABLE {prefix}_{to_table}_{self._name}_Rel(FROM {self._name} TO {to_table} {',' + extra_fields if extra_fields else ''})"
        )

    def add(self, params: dict):
        stmt = ""
        for column in self._columns:
            if column.name in params:
                stmt = f"{stmt+',' if stmt else ''}{column.name}:${column.name}"

        self._conn.execute(
            query=f"CREATE (u:{self._name} {{ {stmt} }});",
            parameters=params,
        )

    def add_relation(
        self, to_table: str, parent_value, child_value, file_path: str, prefix: str
    ):
        condition = "u1.file_path = $file_path AND u2.file_path = $file_path"
        params = {"file_path": file_path}
        if hasattr(parent_value, "lineno"):
            params["u1_lineno"] = parent_value.lineno
            condition = f"{condition} AND u1.lineno = $u1_lineno"
        if hasattr(child_value, "lineno"):
            params["u2_lineno"] = child_value.lineno
            condition = f"{condition} AND u2.lineno = $u2_lineno"
        self._conn.execute(
            query=f"""
                MATCH (u1:{self._name}), (u2:{to_table}) WHERE 
                {condition}
                CREATE (u1)-[:{prefix}_{to_table}_{self._name}_Rel]->(u2)
                """,
            parameters=params,
        )

    @staticmethod
    def _raise_error(error: str):
        logger.error(error)
        raise AttributeError(error)
