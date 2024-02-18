from abc import abstractmethod

from loguru import logger

from iacparsers.ansible.ansible_security_check_core import AnsibleSecurityCheckCore
from iacparsers.linux_file_permission import LinuxFilePermissionValidation
from iacparsers.vulnerability_definition import VulnerabilityDefinition


class AnsiblePermissionCore(AnsibleSecurityCheckCore):
    @classmethod
    @abstractmethod
    def _get_security_checks(cls) -> list:
        raise NotImplementedError()

    @classmethod
    def _security_check_file_permissions(
        cls,
        file_name: str,
        component: dict,
        module_name: str = "",
    ):
        logger.info(f"Checking {component.get('name')} in {file_name}")
        mode = component.get(module_name).get("mode")
        if mode and LinuxFilePermissionValidation.validate_permissions(
            permissions=mode
        ):
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Ansible",
                vulnerability_type="Improper Preservation of Permissions",
                severity="High",
                cwe="CWE-281",
                module=module_name,
                vulnerability=mode,
                line_of_code=component.get("__line__"),
            )
        if not mode:
            # If mode is not specified and the destination file does not exist,
            # the default umask on the system will be used when setting the mode for the newly created file
            return VulnerabilityDefinition(
                file_path=file_name,
                category="Ansible",
                vulnerability_type="Incorrect Default Permissions",
                severity="Medium",
                cwe="CWE-276",
                module=module_name,
                vulnerability=mode,
                line_of_code=component.get("__line__"),
            )
