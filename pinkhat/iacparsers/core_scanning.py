from pathlib import Path

from loguru import logger

from pinkhat.iacparsers.issue_definition import IssueDefinition
from pinkhat.iacparsers.scanner.certificate_core import CertificateCore
from pinkhat.iacparsers.scanner.terraform_core import TerraformCore
from pinkhat.iacparsers.utils.policy_as_code.policy_as_code_rule_loader import (
    TFRuleLoader,
)
from pinkhat.iacparsers.scanner.yaml_core import YamlFile


class CoreScanning:
    SCANNERS = [TerraformCore, CertificateCore, YamlFile]

    def __init__(self):
        self._rules = TFRuleLoader()
        self._results: list[IssueDefinition] = []

    def start_scanning(self, path: str) -> bool:
        self._rules.load_rules()
        try:
            child = Path(path)
            if child.is_file():
                self._scan_file(child=child)
            else:
                self._get_all_files(path=path)
        except Exception as e:
            logger.error(str(e))
            return False
        return True

    def _get_all_files(self, path: str):
        for child in Path(path).rglob("*.*"):
            if child.is_file():
                self._scan_file(child)
            else:
                self._get_all_files(path=str(child))

    def _scan_file(self, child):
        logger.info(f"Parsing {child}")
        for scanner in self.SCANNERS:
            self._results += scanner(rules=self._rules, child=child).run_scan()

    def get_vulnerabilities(self) -> list[IssueDefinition]:
        return self._results

    def get_vulnerabilities_dict(self) -> list[dict]:
        return [result.__dict__ for result in self._results]
