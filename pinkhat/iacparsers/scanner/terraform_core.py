import re
from pathlib import Path

import hcl2
from lark import UnexpectedInput
from loguru import logger

from pinkhat.iacparsers.issue_definition import IssueDefinition
from pinkhat.iacparsers.scanner.core import Core
from pinkhat.iacparsers.utils.policy_as_code.policy_as_code_rule_loader import TFRuleLoader


class TerraformCore(Core):
    FILE_EXTENSION = [".tf"]

    def __init__(self, rules: TFRuleLoader, child: Path):
        super().__init__(rules=rules, child=child)

    def run_scan(self) -> list[IssueDefinition]:
        if self._child.suffix not in self.FILE_EXTENSION:
            logger.error(
                f"Unknown file type extension for terraform {self._child} extension {self._child.suffix}"
            )
            return []
        terraform_objects: dict = self._load_terraform_file()
        for terraform_output in terraform_objects.get("output", []):
            self._parse_terraform_output(tf_output=terraform_output)
        for terraform_resource in terraform_objects.get("resource", []):
            self._parse_terraform_resource(tf_resource=terraform_resource)
        return list(self._policy_validator.check_policies(category="terraform"))

    def _load_terraform_file(self) -> dict:
        """
        Function returns a dict with terraform objects i.e.
        1. variable
        2. output
        3. resource
        4. etc.
        """
        with self._child.open() as file:
            try:
                return hcl2.loads(text=file.read(), with_meta=True)
            except UnexpectedInput as e:
                logger.error(str(e))
                raise ValueError(str(e))
            # TODO: Check if other exceptions might occur
            #  except UnexpectedCharacters as e:
            #   logger.error(str)``UnexpectedToken``, or ``UnexpectedEOF``.
            #   For convenience, these sub-exceptions also inherit from ``ParserError`` and ``LexerError``.

    def _parse_terraform_output(self, tf_output: dict):
        """
        Function iterates over an output elements and finds dependencies or an object without children.
        More information about terraform output data
        https://developer.hashicorp.com/terraform/language/values/outputs
        """
        for tf_module, component in tf_output.items():
            value = component.get("value")
            if not value:
                logger.error(f"There is no value for terraform output {tf_module}")
                continue
            if not (str == type(value) or dict == type(value)):
                logger.error(
                    f"Wrong value type in terraform output {tf_module} - type {type(value)}"
                )
                continue
            # This guy might be tricky, Somebody might not provide the right reference format
            # output "instance_ip_addr" {
            #     value = aws_instance.server.private_ip
            # }
            match: re.Match = re.search(
                pattern="\\${([a-z0-9_]*)\\.([a-z0-9_]*)\\.([a-z_]*)}",
                string=value,
                flags=re.IGNORECASE,
            )
            if not match:
                logger.error(
                    f"Bad output value. It doesn't follow the naming convention - {value}"
                )
                continue
            self._graph_builder.add_graph_object(
                name=tf_module,
                link=f"output.{match.group(1)}",
                child_name=f"{match.group(1)}.{match.group(2)}",
                object_in_graph=component,
            )

    def _parse_terraform_resource(self, tf_resource: dict):
        """
        Function iterates over a resource elements and finds dependencies or an object without children

        The function works in two steps:
        1. Create a new object in graph
        2. Go through all values in a resource and try to find reference to another object
        3. If found then add a link.
            a. if the linked object doesn't exist then it creates an empty one
            b. if the linked object then it just adds a reference to it.
        """
        for tf_module, component in tf_resource.items():
            for component_name, component_values in component.items():
                # Add an element on the beginning of the loop
                self._graph_builder.add_graph_object(
                    name=f"{tf_module}.{component_name}",
                    link=tf_module,
                    child_name=None,
                    object_in_graph=component_values,
                )
                self._build_terraform_graph(
                    tf_module=tf_module,
                    component_name=component_name,
                    component=component_values,
                    values=component_values.values(),
                )

    def _build_terraform_graph(
        self, tf_module: str, component_name: str, component: dict, values: list
    ):
        for value in values:
            if list == type(value):
                self._build_terraform_graph(
                    tf_module=tf_module,
                    component_name=component_name,
                    component=component,
                    values=value,
                )
            elif dict == type(value):
                self._build_terraform_graph(
                    tf_module=tf_module,
                    component_name=component_name,
                    component=component,
                    values=value.values(),
                )
            elif str == type(value):
                match: re.Match
                if match := re.search(
                    pattern="\\${([a-z_]*)\\.([a-z_]*)\\.([a-z_]*)}",
                    string=value,
                    flags=re.IGNORECASE,
                ):
                    self._graph_builder.add_graph_object(
                        name=f"{tf_module}.{component_name}",
                        link=tf_module,
                        child_name=f"{match.group(1)}.{match.group(2)}",
                        object_in_graph=component,
                    )
