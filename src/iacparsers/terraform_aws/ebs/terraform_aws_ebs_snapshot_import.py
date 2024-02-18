from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_core import (
    TerraformAwsEbsEncryptionCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformAwsEbsSnapshotImport(TerraformAwsEbsEncryptionCore):
    """
    CIS Control 2.2.1 Ensure EBS volume encryption is enabled (Automated)
    Description of *aws_ebs_snapshot_import* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_import

    Class checks aws security checks
    encrypted: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_ebs_snapshot_import"
    SECURITY_CHECKS = [
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsEbsSnapshotImport.security_check_encryption(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
            module_name=TerraformAwsEbsSnapshotImport.MODULE_NAME,
        )
    ]

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS
