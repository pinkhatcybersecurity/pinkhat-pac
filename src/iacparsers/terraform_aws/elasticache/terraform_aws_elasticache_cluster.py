from iacparsers.terraform_aws.terraform_security_check_core import (
    TerraformSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformAwsElastiCacheCluster(TerraformSecurityCheckCore):
    """
    Description of *aws_elasticache_cluster* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster

    Class checks aws security checks
    transit_encryption_enabled: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_elasticache_cluster"
    SECURITY_CHECKS = [
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsElastiCacheCluster._security_check_transit_encryption_enabled(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
        )
    ]

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _security_check_transit_encryption_enabled(
        cls,
        file_name: str,
        terraform_resource_name: dict,
        terraform_resource_values: dict,
    ):
        """
        https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html

        :param file_name:
        :param terraform_resource_name:
        :param terraform_resource_values:
        :return:
        """
        if terraform_resource_values.get("transit_encryption_enabled", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Transit",
                severity="High",
                cwe="CWE-311",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {terraform_resource_name}"
                f" doesn't enable encryption",
                line_of_code=terraform_resource_values.get("__start_line__"),
            )
