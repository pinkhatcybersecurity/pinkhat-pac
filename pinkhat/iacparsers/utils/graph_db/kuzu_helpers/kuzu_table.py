import csv
import os
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
        self._csv_mapping = {}
        self._fd = open(os.path.join("tmp_data", f"{self._name}.csv"), "w", newline="")
        self._csv = csv.writer(self._fd)
        self._csv.writerow(
            [column.name for column in self._columns if column.name != "p_id"]
        )
        self._p_id = -1

    @property
    def name(self):
        return self._name

    def p_id(self):
        return self._p_id

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
        rel_name = self._create_rel_file(to_table, prefix, extra_fields)
        self._conn.execute(
            f"CREATE REL TABLE {rel_name} (FROM {self._name} TO {to_table}, "
            f"_tail INT {',' + extra_fields if extra_fields else ''}, ONE_ONE)"
        )

    def _create_rel_file(self, to_table: str, prefix: str, extra_fields: str) -> str:
        rel_name = f"{prefix}_{self._name}_Rel_{self._name}_{to_table}"
        _fd = open(os.path.join("tmp_data", "rels", f"{rel_name}.csv"), "w", newline="")
        _csv = csv.writer(_fd)
        if rel_name not in self._csv_mapping:
            order = ["p_id", "c_id", "_tail"] + [
                field.lstrip().split(" ")[0] for field in extra_fields.split(",")
            ]
            _csv.writerow(order)
            self._csv_mapping[rel_name.lower()] = {
                "fd": _fd,
                "csv": _csv,
                "order": order,
            }
        return rel_name

    def create_relationship_group(
        self, to_table: list[str], prefix: str, extra_fields: str = None
    ):
        if type(to_table) != list:
            self._raise_error(error=f"To table must be a list is {type(to_table)}")
        if not to_table:
            self._raise_error(error="Relationship table is empty")
        # Relationship group requires at least two elements
        if len(to_table) == 1:
            self.create_relationship(
                to_table=to_table[0], prefix=prefix, extra_fields=extra_fields
            )
            return
        from_to: str = ""
        for table in to_table:
            if not re.search(r"^[A-Za-z0-9_]*$", table):
                self._raise_error(error=f"The table name is not alpha {table}")
            from_to = (
                f"{from_to}, FROM {self._name} TO {table}"
                if from_to
                else f"FROM {self._name} TO {table}"
            )
            self._create_rel_file(table, prefix, extra_fields)
        self._conn.execute(
            f"CREATE REL TABLE GROUP {prefix}_{self._name}_Rel ({from_to}, "
            f" _tail INT {',' + extra_fields if extra_fields else ''})"
        )

    def save(self, params: dict):
        self._csv.writerow(
            [
                params.get(column.name)
                for column in self._columns
                if column.name != "p_id"
            ]
        )
        # The table automatically adds and increment p_id but this field
        # is used in save_relation
        self._p_id += 1

    def save_relation(
        self,
        table: str,
        parent_value,
        child_value,
        c_id: int,
        file_path: str,
        prefix: str,
        tail: int = 0,
        extra_field: dict = None,
    ):
        rel_name = f"{prefix}_{self._name}_Rel_{self._name}_{table}"
        if rel := self._csv_mapping.get(rel_name.lower()):
            """
            There are a few corner cases for example:
            a = 1
            a = a + 1
            So, if there are only two factors like line of code and file path in the where parameter
            then two elements will be returned for line number 2. That's the reason why more factors
            must be used in the SQL query, if the graph is generated. For this reason tail has been added.
            """
            params = {
                "p_id": self.p_id(),
                "c_id": c_id,
                "file_path": file_path,
                "lineno": (
                    parent_value.lineno if hasattr(parent_value, "lineno") else None
                ),
                "_tail": tail,
            }
            if extra_field:
                params.update(extra_field)
            if hasattr(child_value, "lineno"):
                params["lineno"] = child_value.lineno
            rel["csv"].writerow([params.get(order) for order in rel["order"]])
        else:
            logger.error(f"Relationship missing {rel_name}")

    @staticmethod
    def _raise_error(error: str):
        logger.error(error)
        raise AttributeError(error)

    def close_fd(self):
        for mapping in self._csv_mapping.values():
            mapping["fd"].close()
        self._fd.close()
