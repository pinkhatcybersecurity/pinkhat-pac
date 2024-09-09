import importlib
import os
import time
import token
import tokenize
from pathlib import Path
from typing import Type

from loguru import logger
from pegen.build import build_python_parser_and_generator
from pegen.parser import Parser
from pegen.tokenizer import Tokenizer

VERBOSE_PEG_PARSER = os.getenv("VERBOSE_PEG_PARSER", 0)


class Grammar:
    """
    pegen is a new way of parsing files. It has been added to CPython sometime ago
    https://devguide.python.org/internals/parser/
    https://peps.python.org/pep-0617/
    The mechanism can be used for many different purposes
    """

    def __init__(self):
        verbose = VERBOSE_PEG_PARSER
        self._verbose_tokenizer = verbose >= 3
        self._verbose_parser = verbose == 2 or verbose >= 4
        self._grammar_files = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data"
        )
        self._parser_files = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "parsers"
        )
        self._gram_loaded_modules = []

    def generate_parser(self):
        logger.info(f"Generating grammar files")
        self._parse_grammar_file(grammar_file=self._grammar_files)

    def _parse_grammar_file(self, grammar_file):
        """
        Function goes over all files and folders in peg/data folder and finds .gram files.
        Then it automatically generates python parser files
        """
        for child in Path(grammar_file).rglob("*.*"):
            if child.is_file():
                if child.suffix == ".gram":
                    logger.info(f"Loading grammar file {child}")
                    gen_script_file_path = os.path.join(
                        self._parser_files, f"{child.name.replace('.', '_')}.py"
                    )
                    # It will generate a python script. There is a risk about file permissions. It might have rw-rw-r-
                    # So, it is required to pass descriptor instead of file path. In the descriptor it is possible to
                    # define permissions. 0o640 should be good -rw-r--.
                    descriptor = os.open(
                        path=gen_script_file_path,
                        flags=(os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                        mode=0o640,
                    )
                    grammar, parser, tokenizer, gen = build_python_parser_and_generator(
                        grammar_file=str(child),
                        output_file=descriptor,
                        verbose_tokenizer=self._verbose_tokenizer,
                        verbose_parser=self._verbose_parser,
                        skip_actions=False,
                    )
                    cls_name = grammar.metas.get("class", "GeneratedParser")
                    module = (
                        gen_script_file_path.replace(f"{os.getcwd()}{os.sep}", "")
                        .replace(".py", "")
                        .replace(os.sep, ".")
                    )
                    self._gram_loaded_modules.append(
                        {
                            "cls_name": cls_name,
                            "module": importlib.import_module(module),
                        }
                    )
            else:
                self._parse_grammar_file(grammar_file=str(child))

    def simple_parser_main(self, file_path: str):
        return [
            self._simple_parser_main(
                parser_class=getattr(module.get("module"), module.get("cls_name")),
                file_path=file_path,
            )
            for module in self._gram_loaded_modules
        ]

    def _simple_parser_main(
        self, parser_class: Type[Parser], file_path: str
    ) -> str | None:
        t0 = time.time()
        # tree = None

        with open(file_path) as file:
            tokengen = tokenize.generate_tokens(file.readline)
            tokenizer = Tokenizer(tokengen, verbose=self._verbose_tokenizer)
            parser = parser_class(tokenizer, verbose=self._verbose_parser)
            tree = parser.start()

        t1 = time.time()

        if not tree:
            err = parser.make_syntax_error(message=file_path)
            logger.error(err.msg)
            return
        Grammar.performance_metrics(parser, t0, t1, tokenizer)
        return tree
        # return ast.dump(tree, True, True)

    @staticmethod
    def performance_metrics(parser, t0, t1, tokenizer):
        delta = t1 - t0
        diagnose = tokenizer.diagnose()
        number_of_lines = diagnose.end[0]
        if diagnose.type == token.ENDMARKER:
            number_of_lines -= 1
        logger.debug(f"Total time: {delta:.3f} sec; {number_of_lines} lines", end="")
        if delta:
            logger.debug(f"; {number_of_lines / delta:.0f} lines/sec")
        logger.debug(
            f"Caches sizes: token array : {len(tokenizer._tokens):10} cache : {len(parser._cache):10}"
        )
