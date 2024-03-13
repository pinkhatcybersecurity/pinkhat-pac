from iacparsers.terraform_aws.ebs.terraform_aws_ebs_encryption_core import (
    TFAwsEbsEncryptionCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFAwsElastiCacheReplicationGroup(TFAwsEbsEncryptionCore):
    """
    Description of *aws_elasticache_cluster* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster

    Class checks aws security checks
    transit_encryption_enabled: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_elasticache_cluster"
    SECURITY_CHECKS = [
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsElastiCacheReplicationGroup._sec_check_transit_encryption_enabled(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsElastiCacheReplicationGroup._sec_check_at_rest_encryption_enabled(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
    ]

    @classmethod
    def _get_sec_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _sec_check_at_rest_encryption_enabled(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        if tf_resource_values.get("at_rest_encryption_enabled", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Rest",
                severity="High",
                cwe="CWE-311",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                f" doesn't enable encryption",
                line_of_code=tf_resource_values.get("__start_line__"),
            )

    @classmethod
    def _sec_check_transit_encryption_enabled(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html

        :param file_name:
        :param tf_resource_name:
        :param tf_resource_values:
        :return:
        """
        if tf_resource_values.get("transit_encryption_enabled", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Transit",
                severity="High",
                cwe="CWE-311",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                f" doesn't enable encryption",
                line_of_code=tf_resource_values.get("__start_line__"),
            )
