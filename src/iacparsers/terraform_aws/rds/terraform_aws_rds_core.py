from abc import abstractmethod

from iacparsers.terraform_aws.terraform_security_check_core import (
    TFSecurityCheckCore,
)
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFAwsRdsCore(TFSecurityCheckCore):
    # The following log types are supported by terraform
    CLOUD_WATCH_LOGS_EXPORT = {"audit", "error", "general", "slowquery", "postgresql"}

    @classmethod
    @abstractmethod
    def _get_sec_checks(cls) -> list:
        raise NotImplementedError()

    @classmethod
    def _sec_check_deletion_protection_enabled(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
        module_name: str = "",
    ):
        if tf_resource_values.get("deletion_protection", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Protect Recovery Data",
                severity="High",
                cwe="CWE-281",
                module=module_name,
                vulnerability=f"Resource {module_name} name: {tf_resource_name}"
                f" doesn't enable deletion protection",
                line_of_code=tf_resource_values.get("__start_line__"),
            )

    @classmethod
    def _sec_check_storage_encrypted(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
        module_name: str = "",
    ):
        if tf_resource_values.get("storage_encrypted", False) is False:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Encrypt Sensitive Data at Rest",
                severity="High",
                cwe="CWE-311",
                module=module_name,
                vulnerability=f"Resource {module_name} name: {tf_resource_name}"
                f" doesn't enable encryption",
                line_of_code=tf_resource_values.get("__start_line__"),
            )

    @classmethod
    def _sec_check_enabled_cloudwatch_logs_exports(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
        module_name: str = "",
    ):
        cloud_watch_logs = tf_resource_values.get("enabled_cloudwatch_logs_exports")
        vulnerability = cls._validate_cloud_watch_exports(
            cloud_watch_logs=cloud_watch_logs,
            module_name=module_name,
            tf_resource_name=tf_resource_name,
            tf_resource_values=tf_resource_values,
        )
        if vulnerability:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Audit Log Management",
                severity="High",
                cwe="CWE-281",
                module=module_name,
                vulnerability=vulnerability,
                line_of_code=tf_resource_values.get("__start_line__"),
            )

    @classmethod
    def _validate_cloud_watch_exports(
        cls,
        cloud_watch_logs,
        module_name,
        tf_resource_name,
        tf_resource_values,
    ) -> str | None:
        if not cloud_watch_logs:
            return f"Resource {module_name} name: {tf_resource_name} doesn't send logs to cloud watch"
        exports = (
            cls.CLOUD_WATCH_LOGS_EXPORT
            - set(cloud_watch_logs)
            - set(
                []
                if "postgresql" in tf_resource_values.get("engine")
                else ["postgresql"]
            )
        )
        if exports:
            return (
                f"Resource {module_name} name: {tf_resource_name} "
                f"doesn't send logs to cloud watch for {sorted(exports)}"
            )

    @classmethod
    def _sec_check_backup_retention_period(
        cls,
        file_name: str,
        tf_resource_name: dict,
        tf_resource_values: dict,
        module_name: str = "",
    ):
        if tf_resource_values.get("backup_retention_period", 0) <= 1:
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Terraform AWS",
                vulnerability_type="Data Recovery",
                severity="High",
                cwe="CWE-664",
                module=module_name,
                vulnerability=f"Resource {module_name} name: {tf_resource_name}"
                f" insufficient data recovery retention period",
                line_of_code=tf_resource_values.get("__start_line__"),
            )
