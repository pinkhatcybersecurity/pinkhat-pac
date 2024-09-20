import os

import pandas

from pinkhat.iacparsers.utils.graph_db.graph_db import GraphDb
from pinkhat.iacparsers.utils.peg.grammar import Grammar

graph_db: GraphDb
names = [
    {
        "_label": "Name",
        "p_id": 0,
        "col_offset": 0,
        "end_col_offset": 1,
        "end_lineno": 1,
        "id": "e",
        "lineno": 1,
        "file_path": "tests/graph_ast_python/test_files/simple_assign.py",
    },
    {
        "_label": "Name",
        "col_offset": 0,
        "end_col_offset": 1,
        "end_lineno": 2,
        "file_path": "tests/graph_ast_python/test_files/simple_assign.py",
        "id": "g",
        "lineno": 2,
        "p_id": 1,
    },
    {
        "_label": "Name",
        "col_offset": 4,
        "end_col_offset": 5,
        "end_lineno": 2,
        "file_path": "tests/graph_ast_python/test_files/simple_assign.py",
        "id": "e",
        "lineno": 2,
        "p_id": 2,
    },
]


def test_run_parser():
    global graph_db
    file_path = os.path.join(
        "tests", "graph_ast_python", "test_files", "simple_assign.py"
    )
    grammar: Grammar = Grammar()
    graph_db = GraphDb()
    grammar.generate_parser()
    graph_db.initialize()
    tree = grammar.simple_parser_main(file_path=file_path)
    graph_db.add_entries(tree=tree, file_path=file_path)


def test_names():
    global graph_db
    df: pandas.DataFrame = graph_db.get_as_df(
        query="MATCH (u:Name) RETURN * ORDER BY u.p_id"
    )
    values = df.values.tolist()
    assert len(values) == len(names)
    for index in range(0, len(values)):
        value = values[index][0]
        assert value["_label"] == names[index]["_label"]
        assert value["col_offset"] == names[index]["col_offset"]
        assert value["end_col_offset"] == names[index]["end_col_offset"]
        assert value["end_lineno"] == names[index]["end_lineno"]
        assert value["file_path"] == names[index]["file_path"]
        assert value["id"] == names[index]["id"]
        assert value["lineno"] == names[index]["lineno"]
        assert value["p_id"] == names[index]["p_id"]
