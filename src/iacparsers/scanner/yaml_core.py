from pathlib import Path

import yaml

from iacparsers.issue_definition import IssueDefinition
from iacparsers.scanner.core import Core
from iacparsers.utils.policy_as_code.policy_as_code_rule_loader import TFRuleLoader
from iacparsers.utils.yaml_safe_line_loader import SafeLineLoader


class YamlFile(Core):
    FILE_EXTENSION = [".yaml", ".yml"]

    def __init__(self, rules: TFRuleLoader, child: Path):
        super().__init__(rules=rules, child=child)

    def run_scan(self) -> list[IssueDefinition]:
        if self._child.suffix not in self.FILE_EXTENSION:
            return []
        with self._child.open() as file:
            self._graph_builder.add_graph_object(
                name="",
                child_name=None,
                link="yaml",
                object_in_graph=yaml.load(file.read(), Loader=SafeLineLoader),
            )
        return list(self._policy_validator.check_policies(category="yaml"))
