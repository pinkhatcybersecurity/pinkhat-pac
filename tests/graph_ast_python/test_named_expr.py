import os

import pandas

from pinkhat.iacparsers.utils.graph_db.graph_db import GraphDb
from pinkhat.iacparsers.utils.peg.grammar import Grammar
from tests.graph_ast_python.utils import create_graph_db, compare_df_output

named_expr_compare = [
    [
        {
            "_label": "NamedExpr",
            "p_id": 11,
            "col_offset": 7,
            "end_col_offset": 29,
            "end_lineno": 21,
            "lineno": 21,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
        },
        {
            "_label": "Compare",
            "p_id": 0,
            "col_offset": 6,
            "end_col_offset": 40,
            "end_lineno": 21,
            "lineno": 21,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
        },
        {
            "_label": "Left_Compare_Rel_Compare_NamedExpr",
            "lineno": 21,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
        },
    ]
]
named_expr_assign = [
    [
        {
            "_label": "NamedExpr",
            "col_offset": 1,
            "end_col_offset": 21,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 0,
        },
        {
            "_label": "Name",
            "p_id": 0,
            "col_offset": 1,
            "end_col_offset": 2,
            "end_lineno": 2,
            "lineno": 2,
            "op": None,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "conversion": None,
            "format_spec": None,
            "kind": None,
            "type": None,
            "n": None,
            "s": None,
            "value": None,
            "attr": None,
            "id": "z",
            "name": None,
            "type_comment": None,
            "simple": None,
            "cause": None,
            "level": None,
            "module": None,
            "annotation": None,
            "arg": None,
            "is_async": None,
            "asname": None,
        },
        {
            "_label": "Target_NamedExpr_Rel_NamedExpr_Name",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 1,
            "end_col_offset": 21,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 0,
        },
        {
            "_label": "NamedExpr",
            "p_id": 2,
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "conversion": None,
            "format_spec": None,
            "kind": None,
            "type": None,
            "n": None,
            "s": None,
            "value": None,
            "attr": None,
            "id": None,
            "name": None,
            "type_comment": None,
            "simple": None,
            "cause": None,
            "level": None,
            "module": None,
            "annotation": None,
            "arg": None,
            "is_async": None,
            "asname": None,
        },
        {
            "_label": "Value_NamedExpr_Rel_NamedExpr_NamedExpr",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "p_id": 1,
            "col_offset": 7,
            "end_col_offset": 20,
            "end_lineno": 2,
            "lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
        },
        {
            "_label": "Name",
            "col_offset": 7,
            "end_col_offset": 8,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "id": "y",
            "lineno": 2,
            "p_id": 1,
        },
        {
            "_label": "Target_NamedExpr_Rel_NamedExpr_Name",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 7,
            "end_col_offset": 20,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 1,
        },
        {
            "_label": "NamedExpr",
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "Value_NamedExpr_Rel_NamedExpr_NamedExpr",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "NamedExpr",
            "p_id": 0,
            "col_offset": 1,
            "end_col_offset": 21,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
        {
            "_label": "Value_NamedExpr_Rel_NamedExpr_NamedExpr",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "Constant",
            "col_offset": 18,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 0,
        },
        {
            "_label": "Value_NamedExpr_Rel_NamedExpr_Constant",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "Expr",
            "p_id": 0,
            "col_offset": 0,
            "end_col_offset": 22,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
        {
            "_label": "Value_Expr_Rel_Expr_NamedExpr",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "NamedExpr",
            "col_offset": 7,
            "end_col_offset": 20,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 1,
        },
        {
            "_label": "Value_NamedExpr_Rel_NamedExpr_NamedExpr",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
    [
        {
            "_label": "NamedExpr",
            "col_offset": 13,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "Name",
            "col_offset": 13,
            "end_col_offset": 14,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "id": "x",
            "lineno": 2,
            "p_id": 2,
        },
        {
            "_label": "Target_NamedExpr_Rel_NamedExpr_Name",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": 2,
        },
    ],
]


@create_graph_db
def test_named_expr_compare(graph_db: GraphDb, grammar: Grammar):
    file_path = os.path.join("tests", "graph_ast_python", "test_files", "named_expr.py")
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)
    graph_db.copy_data_to_graph_db()
    df: pandas.DataFrame = graph_db.get_as_df(
        query="MATCH (a:NamedExpr)-[b:Left_Compare_Rel]-(c:Compare) RETURN * ORDER BY a.p_id"
    )
    compare_df_output(df=df, test_data=named_expr_compare)


@create_graph_db
def test_named_expr_assign(graph_db: GraphDb, grammar: Grammar):
    # Testing
    # (z := (y := (x := 0)))
    file_path = os.path.join("tests", "graph_ast_python", "test_files", "named_expr.py")
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)
    graph_db.copy_data_to_graph_db()
    df: pandas.DataFrame = graph_db.get_as_df(
        query="MATCH (a:NamedExpr)-[b]-(c) WHERE a.lineno=2 RETURN * ORDER BY a.p_id, c.p_id"
    )
    compare_df_output(df=df, test_data=named_expr_assign)
