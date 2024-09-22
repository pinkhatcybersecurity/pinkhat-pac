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
