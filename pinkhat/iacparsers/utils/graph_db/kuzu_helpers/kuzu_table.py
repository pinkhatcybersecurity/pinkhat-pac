import re

from kuzu import Connection
from loguru import logger

from iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column


class Table:
    _PREFIXES = ["lineno", "col_offset", "end_lineno", "end_col_offset"]

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
            f"CREATE REL TABLE {prefix}_{to_table}_{self._name}_Rel(FROM {self._name} TO {to_table}"
            f" {',' + extra_fields if extra_fields else ''}, ONE_ONE)"
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
        """
        There are a few corner cases for example:
        a = 1
        a = a + 1
        So, if there are only two factors like line of code and file path in the where parameter
        then two elements will be returned for line number 2. That's the reason why more factors
        must be used in the SQL query, if the graph is generated.
        """
        if hasattr(parent_value, "lineno"):
            for prf in self._PREFIXES:
                params[f"u1_{prf}"] = getattr(parent_value, prf)
                condition = f"{condition} AND u1.{prf} = $u1_{prf}"
        if hasattr(child_value, "lineno"):
            for prf in self._PREFIXES:
                params[f"u2_{prf}"] = getattr(child_value, prf)
                condition = f"{condition} AND u2.{prf} = $u2_{prf}"
        self._conn.execute(
            query=f"""
                MATCH (u1:{self._name}), (u2:{to_table}) WHERE 
                {condition}
                CREATE (u1)-[:{prefix}_{to_table}_{self._name}_Rel {{file_path:'{file_path}'}}]->(u2)
                """,
            parameters=params,
        )

    @staticmethod
    def _raise_error(error: str):
        logger.error(error)
        raise AttributeError(error)
