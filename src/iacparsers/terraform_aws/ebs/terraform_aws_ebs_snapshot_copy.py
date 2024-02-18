from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_core import (
    TerraformAwsEbsEncryptionCore,
)
from iacparsers.terraform_aws.terraform_security_check_core import (
    TerraformSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformAwsEbsSnapshotCopy(TerraformAwsEbsEncryptionCore):
    """
    CIS Control 2.2.1 Ensure EBS volume encryption is enabled (Automated)
    Description of *aws_ebs_snapshot_copy* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_copy

    Class checks aws security checks
    encrypted: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_ebs_snapshot_copy"
    SECURITY_CHECKS = [
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsEbsSnapshotCopy.security_check_encryption(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
            module_name=TerraformAwsEbsSnapshotCopy.MODULE_NAME,
        )
    ]

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS
