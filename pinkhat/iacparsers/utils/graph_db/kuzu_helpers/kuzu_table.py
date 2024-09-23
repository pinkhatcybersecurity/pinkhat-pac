import re

from kuzu import Connection
from loguru import logger

from pinkhat.iacparsers.utils.graph_db.kuzu_helpers.kuzu_column import Column


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

    def create_relationship_group(
        self, to_table: list[str], prefix: str, extra_fields: str = None
    ):
        if type(to_table) != list:
            self._raise_error(error=f"To table must be a list is {type(to_table)}")
        from_to: str = ""
        for table in to_table:
            if not re.search(r"^[A-Za-z0-9_]*$", table):
                self._raise_error(error=f"The table name is not alpha {table}")
            from_to = (
                f"{from_to}, FROM {self._name} TO {table}"
                if from_to
                else f"FROM {self._name} TO {table}"
            )
        self._conn.execute(
            f"CREATE REL TABLE GROUP {prefix}_{self._name}_Rel ({from_to}, "
            f" _tail INT {',' + extra_fields if extra_fields else ''})"
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

    def add_relation_group(
        self,
        stmt: dict,
        parent_value,
        child_value,
        file_path: str,
        prefix: str,
        extra_field: dict,
    ):
        params = {
            "file_path": file_path,
            "lineno": parent_value.lineno if getattr(parent_value, "lineno") else None,
            "_tail": 0,
        }
        params.update(extra_field)
        extra_params = ",".join([f"{key}: ${key}" for key in params.keys()])
        """
        There are a few corner cases for example:
        a = 1
        a = a + 1
        So, if there are only two factors like line of code and file path in the where parameter
        then two elements will be returned for line number 2. That's the reason why more factors
        must be used in the SQL query, if the graph is generated.
        """
        condition = ""
        if hasattr(parent_value, "lineno"):
            for prf in self._PREFIXES:
                params[f"u1_{prf}"] = getattr(parent_value, prf)
                condition = f"{condition} AND u1.{prf} = $u1_{prf}"
        # The number 1 is the main table, let's start index from 2 for child elements
        index = 2
        for child in child_value:
            # Even if it is a relationship group, then all elements must be added in the separated
            # iterations.
            tmp_stmt = condition
            # It's required to make a copy of the parameters. In the next iteration the previous
            # will still exist, and then it drops an exceptions about that it can't find
            # the parameters in the query
            tmp_params = params.copy()
            if hasattr(child, "lineno"):
                # It has a few parameters required to identify an object and make a relationship
                for prf in self._PREFIXES:
                    tmp_params[f"u{index}_{prf}"] = getattr(child, prf)
                    tmp_stmt = f"{tmp_stmt} AND u{index}.{prf} = $u{index}_{prf}"
            self._conn.execute(
                query=f"""
                    MATCH (u1:{self._name}), (u{index}:{stmt.get(type(child)).TABLE_NAME}) WHERE 
                    u1.file_path = $file_path AND u{index}.file_path = $file_path
                    {tmp_stmt}
                    CREATE (u1)-[u:{prefix}_{self._name}_Rel {{ {extra_params} }}]->(u{index})
                """,
                parameters=tmp_params,
            )
            index += 1
            params["_tail"] += 1

    @staticmethod
    def _raise_error(error: str):
        logger.error(error)
        raise AttributeError(error)
