from iacparsers.terraform_aws.terraform_security_check_core import (
    TFSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFAwsLBListener(TFSecurityCheckCore):
    """
    Description of *aws_lb_listener* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener
    """

    MODULE_NAME = "aws_lb_listener"
    SECURITY_CHECKS = [
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsLBListener._sec_check_protocol(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsLBListener._sec_check_mutual_authentication_ignore_client_certificate_expiry(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
    ]

    @classmethod
    def _get_sec_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _sec_check_protocol(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        Class checks aws security checks
        enable_deletion_protection: should be set to True. Default option is False
        """
        if tf_resource_values.get("protocol", "HTTP") == "HTTP":
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Enable Deletion Protection",
                severity="High",
                cwe="CWE-664",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                f" there is no enabled deletion protection",
                line_of_code=tf_resource_values.get("__start_line__"),
            )

    @classmethod
    def _sec_check_mutual_authentication_ignore_client_certificate_expiry(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        Method verifies if certificate expiry date verification is enabled for mutual authentication
        ignore_client_certificate_expiry - if true bypass expiry date. Default value is false
        """
        if mutual_authentication := tf_resource_values.get("mutual_authentication"):
            if (
                mutual_authentication.get("ignore_client_certificate_expiry", False)
                is True
            ):
                return VulnerabilityDefinition(
                    file_path=file_name,
                    category="Terraform AWS",
                    vulnerability_type="Improper Certificate Validation",
                    severity="Medium",
                    cwe="CWE-295",
                    module=cls.MODULE_NAME,
                    vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                    f" client certificate expiry is ignored.",
                    line_of_code=tf_resource_values.get("__start_line__"),
                )
