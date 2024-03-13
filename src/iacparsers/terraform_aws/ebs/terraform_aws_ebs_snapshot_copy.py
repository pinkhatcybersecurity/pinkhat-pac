from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_core import (
    TFAwsEbsEncryptionCore,
)


class TFAwsEbsSnapshotCopy(TFAwsEbsEncryptionCore):
    """
    CIS Control 2.2.1 Ensure EBS volume encryption is enabled (Automated)
    Description of *aws_ebs_snapshot_copy* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_copy

    Class checks aws security checks
    encrypted: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_ebs_snapshot_copy"
    SECURITY_CHECKS = [
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsEbsSnapshotCopy.security_check_encryption(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
            module_name=TFAwsEbsSnapshotCopy.MODULE_NAME,
        )
    ]

    @classmethod
    def _get_sec_checks(cls) -> list:
        return cls.SECURITY_CHECKS
