import os

import pandas

from pinkhat.iacparsers.utils.graph_db.graph_db import GraphDb
from pinkhat.iacparsers.utils.peg.grammar import Grammar
from tests.graph_ast_python.utils import create_graph_db, compare_df_output

compare_test_data = [
    [
        {
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
            "p_id": 1,
            "s": "1",
            "type": "int",
            "value": "1",
        },
        {
            "_label": "Op_Compare_Rel_Compare_Constant",
            "_tail": 0,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "index": 0,
            "lineno": 1,
            "op": "Lt",
        },
        {
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
            "_label": "Op_Compare_Rel_Compare_Name",
            "_tail": 0,
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
            "p_id": 3,
            "s": "10",
            "type": "int",
            "value": "10",
        },
        {
            "_label": "Op_Compare_Rel_Compare_Constant",
            "_tail": 0,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "index": 1,
            "lineno": 1,
            "op": "LtE",
        },
        {
            "_label": "Name",
            "col_offset": 4,
            "end_col_offset": 5,
            "end_lineno": 1,
            "file_path": os.path.join(
                "tests", "graph_ast_python", "test_files", "simple_compare.py"
            ),
            "id": "a",
            "lineno": 1,
            "p_id": 2,
        },
        {
            "_label": "Op_Compare_Rel_Compare_Name",
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
    graph_db.copy_data_to_graph_db()
    df: pandas.DataFrame = graph_db.get_as_df(
        f"MATCH (a:Compare)-[u2:Op_Compare_Rel]->(b:Constant), (a:Compare)-[u3:Op_Compare_Rel]->(c:Name) "
        f"WHERE u2.index = u3.index "
        f"RETURN * ORDER BY u2.index, u2._tail, u3.index, u3._tail"
    )
    compare_df_output(df=df, test_data=compare_test_data)
