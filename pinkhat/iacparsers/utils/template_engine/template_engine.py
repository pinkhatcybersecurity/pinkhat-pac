import ast
import re
from typing import Any

from jinja2.exceptions import (
    SecurityError,
    TemplateSyntaxError,
    UndefinedError,
    TemplateRuntimeError,
)
from jinja2.sandbox import SandboxedEnvironment
from loguru import logger

from pinkhat.iacparsers.utils.graph_builder.graph_object import GraphObject


class TemplateEngine:
    def __init__(self):
        self._sandbox = SandboxedEnvironment()
        self._sandbox.trim_blocks = True
        self._sandbox.lstrip_blocks = True
        # Setting up filters (pipes) i.e. something | re_search
        self._sandbox.filters["dict_item"] = TemplateEngine.dict_item
        self._sandbox.filters["re_search"] = TemplateEngine.re_search
        self._sandbox.filters["re_match"] = TemplateEngine.re_match
        # Setting up tests i.e.
        # selectattr('destination_type', 're_search', '^(cloudwatch-logs|kinesis-firehose)')
        self._sandbox.tests["startswith"] = TemplateEngine.startswith
        self._sandbox.tests["re_search"] = TemplateEngine.re_search
        self._sandbox.tests["re_match"] = TemplateEngine.re_match
        # Global functions (python function to support optimization operations)
        self._sandbox.globals["any"] = TemplateEngine.do_any
        self._sandbox.globals["bool"] = TemplateEngine.boolean
        self._sandbox.globals["set"] = TemplateEngine.do_set
        self._sandbox.globals["re_match"] = TemplateEngine.re_match
        self._sandbox.globals["re_search"] = TemplateEngine.re_search

    @staticmethod
    def jinja_error_handler(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TemplateSyntaxError as syntax:
                logger.error(str(syntax))
                raise RuntimeError(str(syntax))
            except UndefinedError as undefined:
                logger.error(str(undefined))
                raise RuntimeError(str(undefined))
            except SecurityError as security:
                logger.critical(str(security))
                raise RuntimeError(str(security))
            except TemplateRuntimeError as runtime_error:
                logger.critical(str(runtime_error))
                raise RuntimeError(str(runtime_error))
            except TypeError as type_error:
                # Most likely, an element is None and you would like to use 'in' operator i.e.
                # 'check' in p.get('value') -> p.get('value') returns None
                logger.error(str(type_error))
                raise RuntimeError(str(type_error))

        return inner

    @staticmethod
    def startswith(value: str, other: str) -> bool:
        """
        The function is equivalent to str.startswith

        :return: True/False
        """
        return bool(
            type(value) == str and type(other) == str and value.startswith(other)
        )

    @staticmethod
    def dict_item(value: dict, other: str):
        """
        Function checks for an item in dict. Used in filters
        """
        if dict == type(value):
            return value.get(other)

    @staticmethod
    def boolean(value: Any):
        return bool(value)

    @staticmethod
    def do_set(value: Any):
        return (
            set(value)
            if value and (dict == type(value) or list == type(value))
            else set()
        )

    @staticmethod
    def do_any(value: Any):
        return any(value)

    @staticmethod
    def re_search(value: str, other: str):
        """
        Method finds an occurrence in a provided regex. It must be done in this way due limitations in map function
        helper | map('re_search', 'POSTGRES_PASSWORD\\s+')

        value: provided string
        other: regex
        """
        if not (str == type(value) and type(other) == str):
            return False
        return re.search(pattern=other, string=value) is not None

    @staticmethod
    def re_match(value: str, other: str):
        """
        Method finds an occurrence in a provided regex. It must be done in this way due limitations in map function
        helper | map('re_search', 'POSTGRES_PASSWORD\\s+')

        value: provided string
        other: regex
        """
        if not (str == type(value) and type(other) == str):
            return False
        return re.match(pattern=other, string=value) is not None

    @jinja_error_handler
    def check_condition(
        self, statement: str, this: GraphObject, helper: dict = None
    ) -> bool:
        """
        This part of code is a little bit difficult. I wanted to use conditions in yaml files
        Running regexes and eval doesn't work very well. Eval is very insecure and there are too many
        combinations to kill the application, destroy the system, delete files etc.
        There is more secure version of it, called ast.literal_eval(). Unfortunately it doesn't allow to run
        simple statement such as 'a' == 'a'. So, Jinja2 is helpful here, as a parameter you must put
        an object which will be used, during evaluation process. Jinja2 is quite useful in rendering a page
        content, so some features might be used here.
        """
        result = self._sandbox.from_string(source=f"{{{{ {statement} }}}}").render(
            this=this, helper=helper
        )
        logger.debug(f"check condition result: {result}")
        return result == "True"

    @jinja_error_handler
    def generate_failed_message(self, failed_message_template: str, this: GraphObject):
        if failed_message_template:
            result = self._sandbox.from_string(source=failed_message_template).render(
                this=this
            )
            logger.debug(result)
            return result
        return failed_message_template

    @jinja_error_handler
    def run_helper(self, helper_template: str, this: GraphObject):
        """
        It's really crazy, json.loads doesn't like single quote (') and you must replace it
        with double quotes ("). There is a function called ast.literal_eval but it is not an attack free
        method. Reading the documentation stated that:
        -----------------------------------------------------------------------------------------------
        This function had been documented as “safe” in the past without defining what that meant.
        That was misleading. This is specifically designed not to execute Python code,
        unlike the more general eval(). There is no namespace, no name lookups, or ability to call out.
        But it is not free from attack: A relatively small input can lead to memory exhaustion or to
        C stack exhaustion, crashing the process. There is also the possibility for excessive
        CPU consumption denial of service on some inputs.
        Calling it on untrusted data is thus not recommended.
        -----------------------------------------------------------------------------------------------
        You can read more about it here: https://docs.python.org/3/library/ast.html#ast.literal_eval
        You could run an attack against literal_eval using () * 1000000

        Jinja2 render returns a string, so it's required to validate output. It should start with:
        - "" then it's a string
        - {} then it's a dict
        - [] then it's a list
        - other stuff doesn't work for us
        """
        result = self._sandbox.from_string(source=helper_template).render(this=this)
        logger.debug(f"Output from helper: {result}")
        if not result:
            return
        result = result.lstrip().rstrip()

        if (
            result.startswith(("{", "[", '"')) and result.endswith(("}", "]", '"'))
        ) or result in ["True", "False"]:
            try:
                return ast.literal_eval(ast.parse(result, mode="eval"))
            except (ValueError, TypeError, SyntaxError, MemoryError) as e:
                logger.error(str(e))
            except RecursionError as e:
                """
                >>> import ast
                >>> code = '()' * 1000000
                >>> ast.literal_eval(code)
                Traceback (most recent call last):
                  File "<stdin>", line 1, in <module>
                  File "/usr/lib/python3.12/ast.py", line 66, in literal_eval
                    node_or_string = parse(node_or_string.lstrip(" \t"), mode='eval')
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                  File "/usr/lib/python3.12/ast.py", line 52, in parse
                    return compile(source, filename, mode, flags,
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                RecursionError: maximum recursion depth exceeded during ast construction
                """
                logger.critical(f"Hacker? {str(e)}")
