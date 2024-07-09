from pathlib import Path

from pinkhat.iacparsers.issue_definition import IssueDefinition
from pinkhat.iacparsers.scanner.core import Core
from pinkhat.iacparsers.utils.certificate.certificate_validator import CertificateValidator
from pinkhat.iacparsers.utils.policy_as_code.policy_as_code_rule_loader import TFRuleLoader


class CertificateCore(Core):
    FILE_EXTENSION = [".pem", ".crt", ".der"]

    def __init__(self, rules: TFRuleLoader, child: Path):
        super().__init__(rules=rules, child=child)

    def run_scan(self) -> list[IssueDefinition]:
        if self._child.suffix not in self.FILE_EXTENSION:
            return []
        cert_data = CertificateValidator(
            certificate_path=str(self._child.absolute()),
            graph_builder=self._graph_builder,
        )
        cert_data.load_certificate_data()
        return list(self._policy_validator.check_policies(category="certificate"))
