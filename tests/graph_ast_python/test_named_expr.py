import os

import pandas

from tests.graph_ast_python.create_graph_db import create_graph_db

named_expr_compare = [
    [
        {
            "_id": {"offset": 11, "table": 17},
            "_label": "NamedExpr",
            "p_id": 11,
            "col_offset": 7,
            "end_col_offset": 29,
            "end_lineno": 21,
            "lineno": 21,
            "file_path": "tests/graph_ast_python/test_files/named_expr.py",
        },
        {
            "_id": {"offset": 0, "table": 20},
            "_label": "Compare",
            "p_id": 0,
            "col_offset": 6,
            "end_col_offset": 40,
            "end_lineno": 21,
            "lineno": 21,
            "file_path": "tests/graph_ast_python/test_files/named_expr.py",
        },
        {
            "_src": {"offset": 11, "table": 17},
            "_dst": {"offset": 0, "table": 20},
            "_label": "Left_NamedExpr_Compare_Rel",
            "lineno": None,
            "file_path": "tests/graph_ast_python/test_files/named_expr.py",
        },
    ]
]


@create_graph_db
def test_named_expr_compare(graph_db, grammar):
    file_path = os.path.join("tests", "graph_ast_python", "test_files", "named_expr.py")
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)
    df: pandas.DataFrame = graph_db.get_as_df(
        query="MATCH (a:NamedExpr)-[b]-(c:Compare) RETURN * ORDER BY a.p_id"
    )
    values = df.values.tolist()
    assert len(values) == len(named_expr_compare)
    for index in range(0, len(values)):
        assert values[index] == named_expr_compare[index]
