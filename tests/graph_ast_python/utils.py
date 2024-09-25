import pandas

from pinkhat.iacparsers.utils.graph_db.graph_db import GraphDb
from pinkhat.iacparsers.utils.peg.grammar import Grammar


def create_graph_db(func):
    def wrapper(*args, **kwargs):
        grammar: Grammar = Grammar()
        graph_db = GraphDb()
        grammar.generate_parser()
        graph_db.initialize()
        kwargs["graph_db"] = graph_db
        kwargs["grammar"] = grammar
        return func(*args, **kwargs)

    return wrapper


def compare_df_output(df: pandas.DataFrame, test_data: list):
    values = df.values.tolist()
    assert len(values) == len(test_data)
    for index in range(0, len(values)):
        tests: list = test_data[index]
        assert len(values[index]) == len(test_data[index])
        for index_test in range(0, len(tests)):
            for item, value in tests[index_test].items():
                assert values[index][index_test].get(item) == value
