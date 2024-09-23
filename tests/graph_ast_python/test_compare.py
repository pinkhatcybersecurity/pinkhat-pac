import os

import pandas

from pinkhat.iacparsers.utils.graph_db.graph_db import GraphDb
from pinkhat.iacparsers.utils.peg.grammar import Grammar
from tests.graph_ast_python.create_graph_db import create_graph_db

compare_test_data = [
    [
        {
            "_id": {"offset": 0, "table": 21},
            "_label": "Compare",
            "col_offset": 0,
            "end_col_offset": 11,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "lineno": 1,
            "p_id": 0,
        },
        {
            "_id": {"offset": 0, "table": 25},
            "_label": "Constant",
            "col_offset": 0,
            "end_col_offset": 1,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "kind": None,
            "lineno": 1,
            "n": "1",
            "p_id": 0,
            "s": "1",
            "type": "int",
            "value": "1",
        },
        {
            "_dst": {"offset": 0, "table": 25},
            "_label": "Op_Compare_Rel_Compare_Constant",
            "_src": {"offset": 0, "table": 21},
            "_tail": 0,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "index": 0,
            "lineno": 1,
            "op": "Lt",
        },
        {
            "_id": {"offset": 0, "table": 28},
            "_label": "Name",
            "col_offset": 4,
            "end_col_offset": 5,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "id": "a",
            "lineno": 1,
            "p_id": 0,
        },
        {
            "_dst": {"offset": 0, "table": 28},
            "_label": "Op_Compare_Rel_Compare_Name",
            "_src": {"offset": 0, "table": 21},
            "_tail": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "index": 0,
            "lineno": 1,
            "op": "Lt",
        },
    ],
    [
        {
            "_id": {"offset": 0, "table": 21},
            "_label": "Compare",
            "col_offset": 0,
            "end_col_offset": 11,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "lineno": 1,
            "p_id": 0,
        },
        {
            "_id": {"offset": 1, "table": 25},
            "_label": "Constant",
            "col_offset": 9,
            "end_col_offset": 11,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "kind": None,
            "lineno": 1,
            "n": "10",
            "p_id": 1,
            "s": "10",
            "type": "int",
            "value": "10",
        },
        {
            "_dst": {"offset": 1, "table": 25},
            "_label": "Op_Compare_Rel_Compare_Constant",
            "_src": {"offset": 0, "table": 21},
            "_tail": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "index": 1,
            "lineno": 1,
            "op": "LtE",
        },
        {
            "_id": {"offset": 0, "table": 28},
            "_label": "Name",
            "col_offset": 4,
            "end_col_offset": 5,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "id": "a",
            "lineno": 1,
            "p_id": 0,
        },
        {
            "_dst": {"offset": 0, "table": 28},
            "_label": "Op_Compare_Rel_Compare_Name",
            "_src": {"offset": 0, "table": 21},
            "_tail": 0,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "index": 1,
            "lineno": 1,
            "op": "LtE",
        },
    ],
]


@create_graph_db
def test_compare(graph_db: GraphDb, grammar: Grammar):
    # Testing a case
    # 1 < a <= 10
    file_path = os.path.join(
        "tests", "graph_ast_python", "test_files", "simple_compare.py"
    )
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)
    df: pandas.DataFrame = graph_db.get_as_df(
        f"MATCH (a:Compare)-[u2:Op_Compare_Rel]->(b:Constant), (a:Compare)-[u3:Op_Compare_Rel]->(c:Name) "
        f"WHERE u2.index = u3.index "
        f"RETURN * ORDER BY u2.index, u2._tail"
    )
    values = df.values.tolist()
    assert len(values) == len(compare_test_data)
    for index in range(0, len(values)):
        assert values[index] == compare_test_data[index]
