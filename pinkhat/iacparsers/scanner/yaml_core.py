from pathlib import Path

import yaml

from pinkhat.iacparsers.issue_definition import IssueDefinition
from pinkhat.iacparsers.scanner.core import Core
from pinkhat.iacparsers.utils.policy_as_code.policy_as_code_rule_loader import (
    TFRuleLoader,
)
from pinkhat.iacparsers.utils.yaml_safe_line_loader import SafeLineLoader


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
                # yaml.load might be reported by bandit or other SAST tools
                # and yaml.safe_load is recommended to be used. I need line of code
                # and other features in the future. Unfortunately yaml.safe_load doesn't allow me
                # to add any information about loader. Under the hood, safe_load used SafeLoader in Loader parameter.
                # SafeLineLoader inherit SafeLoader, then the application should be safe.
                object_in_graph=yaml.load(file.read(), Loader=SafeLineLoader),
            )
        return list(self._policy_validator.check_policies(category="yaml"))
