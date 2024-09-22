import ast
import shutil
from pathlib import Path

import kuzu
import pandas
from kuzu import Connection
from loguru import logger

from pinkhat.iacparsers.utils.graph_db.graph_schema.arg_graph_db import ArgGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.assign_graph_db import AssignGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.attribute_graph_db import (
    AttributeGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.binop_graph_db import BinOpGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.bool_op_graph_db import (
    BoolOpGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.call_graph_db import CallGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.class_def_graph_db import (
    ClassDefGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.compare_graph_db import (
    CompareGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.comprehension_graph_db import (
    ComprehensionGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.constant_graph_db import (
    ConstantGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.except_handler_graph_db import (
    ExceptHandlerGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.expr_graph_db import ExprGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.for_graph_db import ForGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.formatted_value_graph_db import (
    FormattedValueGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.function_def_graph_db import (
    FunctionDefGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.global_graph_db import GlobalGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.if_graph_db import IfGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.is_graph_db import IsGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.joinedstr_graph_db import (
    JoinedStrGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.keyword_graph_db import (
    KeywordGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.list_comp_graph_db import (
    ListCompGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.list_graph_db import ListGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.module_graph_db import ModuleGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.name_graph_db import NameGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.named_expr_graph_db import (
    NamedExprGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.raise_graph_db import RaiseGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.return_graph_db import ReturnGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.starred_graph_db import (
    StarredGraphDb,
)
from pinkhat.iacparsers.utils.graph_db.graph_schema.try_graph_db import TryGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.tuple_graph_db import TupleGraphDb
from pinkhat.iacparsers.utils.graph_db.graph_schema.while_graph_db import WhileGraphDb


class GraphDb:
    _DATABASE_NAME = "./scan_db"

    def __init__(self):
        dir_path = Path(self._DATABASE_NAME)
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
        self._db = kuzu.Database(self._DATABASE_NAME)
        self._conn: Connection = kuzu.Connection(self._db)
        self._initialize_stmt()
        self._initialize_expressions()
        self._graph_objects = {
            "module": ModuleGraphDb(conn=self._conn),
        }

    def _initialize_expressions(self):
        self._expressions = {
            ast.BoolOp: BoolOpGraphDb(conn=self._conn),
            ast.NamedExpr: NamedExprGraphDb(conn=self._conn),
            ast.BinOp: BinOpGraphDb(conn=self._conn),
            ast.UnaryOp: None,
            ast.Lambda: None,
            ast.IfExp: None,
            ast.Dict: None,
            ast.Set: None,
            ast.ListComp: ListCompGraphDb(conn=self._conn),
            ast.SetComp: None,
            ast.DictComp: None,
            ast.GeneratorExp: None,
            ast.Await: None,
            ast.Yield: None,
            ast.YieldFrom: None,
            ast.Compare: CompareGraphDb(conn=self._conn),
            ast.Call: CallGraphDb(conn=self._conn),
            ast.FormattedValue: FormattedValueGraphDb(conn=self._conn),
            ast.JoinedStr: JoinedStrGraphDb(conn=self._conn),
            ast.Constant: ConstantGraphDb(conn=self._conn),
            ast.Attribute: AttributeGraphDb(conn=self._conn),
            ast.Subscript: None,
            ast.Starred: StarredGraphDb(conn=self._conn),
            ast.Name: NameGraphDb(conn=self._conn),
            ast.List: ListGraphDb(conn=self._conn),
            ast.Tuple: TupleGraphDb(conn=self._conn),
            ast.Slice: None,
            ast.Module: ModuleGraphDb(conn=self._conn),
        }

    def _initialize_stmt(self):
        self._stmt = {
            ast.FunctionDef: FunctionDefGraphDb(conn=self._conn),
            ast.AsyncFunctionDef: None,
            ast.ClassDef: ClassDefGraphDb(conn=self._conn),
            ast.Return: ReturnGraphDb(conn=self._conn),
            ast.Delete: None,
            ast.Assign: AssignGraphDb(conn=self._conn),
            ast.TypeAlias: None,
            ast.AugAssign: None,
            ast.AnnAssign: None,
            ast.For: ForGraphDb(conn=self._conn),
            ast.AsyncFor: None,
            ast.While: WhileGraphDb(conn=self._conn),
            ast.If: IfGraphDb(conn=self._conn),
            ast.With: None,
            ast.AsyncWith: None,
            ast.Match: None,
            ast.Raise: RaiseGraphDb(conn=self._conn),
            ast.Try: TryGraphDb(conn=self._conn),
            ast.TryStar: None,
            ast.Assert: None,
            ast.Import: None,
            ast.ImportFrom: None,
            ast.Global: GlobalGraphDb(conn=self._conn),
            ast.Nonlocal: None,
            ast.Expr: ExprGraphDb(conn=self._conn),
            ast.Pass: None,
            ast.Break: None,
            ast.Continue: None,
            ast.arg: ArgGraphDb(conn=self._conn),
            ast.keyword: KeywordGraphDb(conn=self._conn),
            ast.ExceptHandler: ExceptHandlerGraphDb(conn=self._conn),
            ast.Is: IsGraphDb(conn=self._conn),
            ast.comprehension: ComprehensionGraphDb(conn=self._conn),
        }

    def initialize(self):
        for stmt in self._stmt.values():
            if stmt:
                stmt.initialize(stmt=self._stmt, expr=self._expressions)
        for expr in self._expressions.values():
            if expr:
                expr.initialize(stmt=self._stmt, expr=self._expressions)
        for stmt in self._stmt.values():
            if stmt and callable(getattr(stmt, "create_rel", None)):
                stmt.create_rel()
        for expr in self._expressions.values():
            if expr and callable(getattr(expr, "create_rel", None)):
                expr.create_rel()

    def add_entries(self, tree: list, file_path: str):
        """
        The function is divided in two stages. In the first stage it adds all elements to the graph database
        During second phase the algorithm can do relationships between elements. There are many different
        combinations in classes and other functions i.e.

        ```{code-block} python
            class big():
                    def __init__(self):
                            print(f"big class {self._value}")

                    _value = "happy string"

            big()
        ```
        Args:
            tree: A dict that contains AST
            file_path: Parsed file

        Returns:

        """
        for value in tree:
            stmt = self._stmt.get(type(value), self._expressions.get(type(value)))
            if stmt:
                stmt.add(value=value, file_path=file_path)
            else:
                logger.error(f"Unknown type {type(value)}")

    def execute(self, query: str):
        response = self._conn.execute(query=query)
        while response.has_next():
            yield response.get_next()

    def get_as_df(self, query: str, params: dict = None) -> pandas.DataFrame:
        resp = self._conn.execute(query=query, parameters=params)
        if resp:
            return resp.get_as_df()

    def close(self):
        if self._conn:
            self._conn.close()
