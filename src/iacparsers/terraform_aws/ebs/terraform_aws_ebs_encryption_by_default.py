from iacparsers.terraform_aws.terraform_security_check_core import (
    TerraformSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformAwsEbsEncryptionByDefault(TerraformSecurityCheckCore):
    """
    CIS Control 2.2.1 Ensure EBS volume encryption is enabled (Automated)
    Description of *aws_ebs_encryption_by_default* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_encryption_by_default

    Class checks aws security checks
    enabled: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_ebs_encryption_by_default"

    SECURITY_CHECKS = [
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsEbsEncryptionByDefault._security_check_ebs_encryption_enabled_by_default(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
        )
    ]

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _security_check_ebs_encryption_enabled_by_default(
        cls,
        file_name: str,
        terraform_resource_name: dict,
        terraform_resource_values: dict,
    ):
        if terraform_resource_values.get("enabled", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Rest",
                severity="High",
                cwe="CWE-311",
                module=TerraformAwsEbsEncryptionByDefault.MODULE_NAME,
                vulnerability=f"Resource {TerraformAwsEbsEncryptionByDefault.MODULE_NAME} {terraform_resource_name}"
                f" disables default encryption for EBS",
                line_of_code=terraform_resource_values.get("__start_line__"),
            )
