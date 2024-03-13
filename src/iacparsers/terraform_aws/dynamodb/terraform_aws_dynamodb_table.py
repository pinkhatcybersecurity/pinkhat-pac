from iacparsers.terraform_aws.terraform_security_check_core import (
    TFSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFAwsDynamodbTable(TFSecurityCheckCore):
    """
    Description of *aws_ebs_snapshot_import* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table

    Class checks aws security checks
    encrypted: should be set to True. Default option is False
    """

    MODULE_NAME = "aws_dynamodb_table"
    SECURITY_CHECKS = [
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsDynamodbTable._sec_check_server_side_protection(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsDynamodbTable._sec_check_deletion_protection_enabled(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
    ]

    @classmethod
    def _get_sec_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _sec_check_deletion_protection_enabled(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        if tf_resource_values.get("deletion_protection_enabled", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="",
                severity="High",
                cwe="CWE-281",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                f" doesn't enable deletion protection for Dynamo table {tf_resource_values.get('name')}",
                line_of_code=tf_resource_values.get("__start_line__"),
            )

    @classmethod
    def _sec_check_server_side_protection(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        server_side_encryption: list = tf_resource_values.get("server_side_encryption")
        if not (
            server_side_encryption
            and server_side_encryption[0].get("enabled", False) is True
        ):
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Rest",
                severity="High",
                cwe="CWE-311",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                f" doesn't enable encryption for Dynamo table {tf_resource_values.get('name')}",
                line_of_code=(
                    server_side_encryption[0].get("__start_line__")
                    if server_side_encryption
                    else tf_resource_values.get("__start_line__")
                ),
            )
