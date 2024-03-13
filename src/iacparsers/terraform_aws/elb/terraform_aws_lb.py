from iacparsers.terraform_aws.terraform_security_check_core import (
    TFSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFAwsLB(TFSecurityCheckCore):
    """
    Description of *aws_lb* terraform module:
    https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb
    """

    APPLICATION_LOAD_BALANCER = "application"
    MODULE_NAME = "aws_lb"
    SECURITY_CHECKS = [
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsLB._sec_check_enable_deletion_protection(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsLB._sec_check_app_load_balancer_access_logs(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsLB._sec_check_app_load_balancer_connection_logs(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
        lambda file_name, tf_resource_name, tf_resource_values: TFAwsLB._sec_check_enable_waf_fail_open(
            file_name=file_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        ),
    ]

    @classmethod
    def _get_sec_checks(cls) -> list:
        return cls.SECURITY_CHECKS

    @classmethod
    def _sec_check_enable_deletion_protection(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        Class checks aws security checks
        enable_deletion_protection: should be set to True. Default option is False
        """
        if tf_resource_values.get("enable_deletion_protection", False) is False:
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
    def _sec_check_app_load_balancer_access_logs(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        Class checks aws security checks
        load_balancer_type: if "application" type, then enabled flag should be set to True in access_logs.
                            Default option is False
        """
        if (
            tf_resource_values.get("load_balancer_type", cls.APPLICATION_LOAD_BALANCER)
            == cls.APPLICATION_LOAD_BALANCER
        ):
            connection_logs: list[dict] = tf_resource_values.get("access_logs")
            if not (connection_logs and connection_logs[0].get("enabled")):
                return VulnerabilityDefinition(
                    file_path=file_name,
                    category="Terraform AWS",
                    vulnerability_type="Disabled Access Logs for Application Load Balancer",
                    severity="High",
                    cwe="",
                    module=cls.MODULE_NAME,
                    vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                    f" disabled Application Load Balancer Access Logs",
                    line_of_code=tf_resource_values.get("__start_line__"),
                )

    @classmethod
    def _sec_check_app_load_balancer_connection_logs(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        Class checks aws security checks
        load_balancer_type: if "application" type, then enabled flag should be set to True. Default option is False
        """
        if (
            tf_resource_values.get("load_balancer_type", cls.APPLICATION_LOAD_BALANCER)
            == cls.APPLICATION_LOAD_BALANCER
        ):
            connection_logs: list[dict] = tf_resource_values.get("connection_logs")
            if not (connection_logs and connection_logs[0].get("enabled")):
                return VulnerabilityDefinition(
                    file_path=file_name,
                    category="Terraform AWS",
                    vulnerability_type="Disabled Connection Logs for Application Load Balancer",
                    severity="High",
                    cwe="",
                    module=cls.MODULE_NAME,
                    vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                    f" has disabled connection log for application load balancer",
                    line_of_code=tf_resource_values.get("__start_line__"),
                )

    @classmethod
    def _sec_check_enable_waf_fail_open(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
    ):
        """
        Class checks aws security checks
        enable_waf_fail_open : flag should be set to False. Default option is False
        """
        if tf_resource_values.get("enable_waf_fail_open", False) is True:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Allow passing requests to targets if it is "
                "unable to forward the request to AWS WAF",
                severity="High",
                cwe="",
                module=cls.MODULE_NAME,
                vulnerability=f"Resource {cls.MODULE_NAME} name: {tf_resource_name}"
                f" Allow passing requests to targets if it is unable to forward the request to AWS WAF",
                line_of_code=tf_resource_values.get("__start_line__"),
            )
