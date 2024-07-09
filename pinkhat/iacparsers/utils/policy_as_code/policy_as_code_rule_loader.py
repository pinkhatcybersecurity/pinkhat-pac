import os
from collections import defaultdict
from pathlib import Path
from typing import Iterator

import msgspec.yaml
from loguru import logger

from pinkhat.iacparsers.utils.policy_as_code.pac_schema.pac_policy_schema import PacPolicySchema
from pinkhat.iacparsers.utils.policy_as_code.policy_data import PolicyData


class TFRuleLoader:
    _POLICIES_DIR = os.path.join("pinkhat", "iacparsers", "policies")

    def __init__(self):
        self._policies: list[PacPolicySchema] = []
        self._rules_dict = {}
        self._pac_modules = defaultdict(list)

    def load_rules(self):
        """
        Function is responsible to parse policies files. It builds a dictionary with all rules.
        """
        self._policies = list(self._parse_policies(path=self._POLICIES_DIR))
        self._build_category_dict()

    def _parse_policies(self, path) -> Iterator[PacPolicySchema]:
        """
        Function goes over all files and folders in iacparsers folder. Finds all yaml files and parse them.
        If the file meets all criteria then it becomes a policy
        """
        for child in Path(path).rglob("*.*"):
            if child.is_file():
                logger.info(f"Loading rule file {child}")
                if child.suffix in [".yaml", ".yml"]:
                    with child.open() as file:
                        try:
                            yield msgspec.yaml.decode(file.read(), type=PacPolicySchema)
                        except msgspec.DecodeError as e:
                            logger.error(
                                f"Error during parsing a file {str(child)} - {str(e)}"
                            )
            else:
                self._parse_policies(path=str(child))

    def _build_category_dict(self):
        for policy_main in self._policies:
            for module in policy_main.policies:
                for rule in module.rules:
                    self._pac_modules[(module.category, rule.link)].append(
                        PolicyData(main=policy_main, policy=module, rule=rule)
                    )

    def get_rule_for_module(self, category: str, link: str) -> list[PolicyData]:
        return self._pac_modules.get((category, link), [])
