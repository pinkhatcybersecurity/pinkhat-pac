from abc import abstractmethod

from iacparsers.terraform_aws.terraform_security_check_core import (
    TFSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFAwsEbsEncryptionCore(TFSecurityCheckCore):
    @classmethod
    @abstractmethod
    def _get_sec_checks(cls) -> list:
        raise NotImplementedError()

    @classmethod
    def security_check_encryption(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
        module_name: str = "",
    ) -> VulnerabilityDefinition:
        if tf_resource_values.get("encrypted", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Rest",
                severity="High",
                cwe="CWE-311",
                module=module_name,
                vulnerability=f"Resource {module_name} name: {tf_resource_name}"
                f" doesn't enable encryption",
                line_of_code=tf_resource_values.get("__start_line__"),
            )
