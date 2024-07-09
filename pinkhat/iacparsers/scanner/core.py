from pathlib import Path

from pinkhat.iacparsers.utils.graph_builder.graph_core import GraphCore
from pinkhat.iacparsers.utils.policy_as_code.policy_as_code_rule_loader import TFRuleLoader
from pinkhat.iacparsers.utils.policy_as_code.policy_validator import PolicyValidator


class Core:
    def __init__(self, rules: TFRuleLoader, child: Path):
        self._rules: TFRuleLoader = rules
        self._child: Path = child
        self._graph_builder: GraphCore = GraphCore()
        self._policy_validator: PolicyValidator = PolicyValidator(
            rules=self._rules, graph_core=self._graph_builder, child=self._child
        )
