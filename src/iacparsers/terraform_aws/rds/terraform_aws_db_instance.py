from iacparsers.terraform_aws.rds.terraform_aws_rds_core import TerraformAwsRdsCore
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformAwsDBInstance(TerraformAwsRdsCore):
    """
    Description of *aws_rds_instance* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance

    Class checks aws security checks
    encrypted: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_rds_instance"
    SECURITY_CHECKS = [
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsDBInstance._security_check_deletion_protection_enabled(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
            module_name=TerraformAwsDBInstance.MODULE_NAME,
        ),
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsDBInstance._security_check_storage_encrypted(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
            module_name=TerraformAwsDBInstance.MODULE_NAME,
        ),
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsDBInstance._security_check_enabled_cloudwatch_logs_exports(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
            module_name=TerraformAwsDBInstance.MODULE_NAME,
        ),
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsDBInstance._security_check_backup_retention_period(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
            module_name=TerraformAwsDBInstance.MODULE_NAME,
        ),
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsDBInstance._security_check_maintenance_window(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
        ),
        lambda file_name, terraform_resource_name, terraform_resource_values: TerraformAwsDBInstance._security_check_publicly_accessible(
            file_name=file_name,
            terraform_resource_name=terraform_resource_name,
            terraform_resource_values=terraform_resource_values,
        ),
    ]

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _security_check_maintenance_window(
        cls,
        file_name: str,
        terraform_resource_name: dict,
        terraform_resource_values: dict,
    ):
        """
        More information about maintenance window from AWS:
        https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates

        :param file_name:
        :param terraform_resource_name:
        :param terraform_resource_values:
        :return:
        """
        if terraform_resource_values.get("maintenance_window") is None:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Maintenance Window for OS patching",
                severity="High",
                cwe="CWE-664",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {terraform_resource_name}"
                f" there is no maintenance window",
                line_of_code=terraform_resource_values.get("__start_line__"),
            )

    @classmethod
    def _security_check_publicly_accessible(
        cls,
        file_name: str,
        terraform_resource_name: dict,
        terraform_resource_values: dict,
    ):
        if terraform_resource_values.get("publicly_accessible") is None:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Publicly accessible database",
                severity="High",
                cwe="CWE-664",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {terraform_resource_name}"
                f" is publicly accessible",
                line_of_code=terraform_resource_values.get("__start_line__"),
            )
