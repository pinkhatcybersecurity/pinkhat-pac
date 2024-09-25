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
            "_label": "Left_NamedExpr_Compare_Rel",
            "lineno": None,
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
            "_label": "Expr",
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 0,
            "conversion": None,
            "end_col_offset": 22,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": None,
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 0,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Value_NamedExpr_Expr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 7,
            "conversion": None,
            "end_col_offset": 20,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": None,
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 1,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Value_NamedExpr_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "_label": "Name",
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 1,
            "conversion": None,
            "end_col_offset": 2,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": "z",
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 2,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Target_Name_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 1,
            "conversion": None,
            "end_col_offset": 21,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": None,
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 0,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Value_NamedExpr_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 13,
            "conversion": None,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": None,
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 2,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Value_NamedExpr_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "_label": "Name",
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 7,
            "conversion": None,
            "end_col_offset": 8,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": "y",
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 1,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Target_Name_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 7,
            "conversion": None,
            "end_col_offset": 20,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": None,
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 1,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Value_NamedExpr_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 18,
            "conversion": None,
            "end_col_offset": 19,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": None,
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": "0",
            "name": None,
            "op": None,
            "p_id": 0,
            "returns": None,
            "s": "0",
            "type": "int",
            "type_comment": None,
            "value": "0",
        },
        {
            "_label": "Value_Constant_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
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
            "annotation": None,
            "arg": None,
            "attr": None,
            "cause": None,
            "col_offset": 13,
            "conversion": None,
            "end_col_offset": 14,
            "end_lineno": 2,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "format_spec": None,
            "id": "x",
            "is_async": None,
            "kind": None,
            "lineno": 2,
            "n": None,
            "name": None,
            "op": None,
            "p_id": 0,
            "returns": None,
            "s": None,
            "type": None,
            "type_comment": None,
            "value": None,
        },
        {
            "_label": "Target_Name_NamedExpr_Rel",
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "named_expr.py"
            ),
            "lineno": None,
        },
    ],
]


@create_graph_db
def test_named_expr_compare(graph_db: GraphDb, grammar: Grammar):
    file_path = os.path.join("tests", "graph_ast_python", "test_files", "named_expr.py")
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)
    df: pandas.DataFrame = graph_db.get_as_df(
        query="MATCH (a:NamedExpr)-[b:Left_NamedExpr_Compare_Rel]-(c:Compare) RETURN * ORDER BY a.p_id"
    )
    compare_df_output(df=df, test_data=named_expr_compare)


@create_graph_db
def test_named_expr_assign(graph_db: GraphDb, grammar: Grammar):
    # Testing
    # (z := (y := (x := 0)))
    file_path = os.path.join("tests", "graph_ast_python", "test_files", "named_expr.py")
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)
    df: pandas.DataFrame = graph_db.get_as_df(
        query="MATCH (a:NamedExpr)-[b]-(c) WHERE a.lineno=2 RETURN * ORDER BY a.p_id"
    )
    compare_df_output(df=df, test_data=named_expr_assign)
