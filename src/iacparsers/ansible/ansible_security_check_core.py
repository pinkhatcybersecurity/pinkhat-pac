from abc import ABC, abstractmethod

from iacparsers.vulnerability_definition import VulnerabilityDefinition


class AnsibleSecurityCheckCore(ABC):
    @classmethod
    @abstractmethod
    def _get_security_checks(cls) -> list:
        raise NotImplementedError()

    @classmethod
    def ansible_resource_parser(
        cls, file_name: str, component: dict
    ) -> list[VulnerabilityDefinition]:
        return [
            vulnerability
            for security_check in cls._get_security_checks()
            if (
                vulnerability := security_check(
                    file_name=file_name,
                    component=component,
                )
            )
            is not None
        ]
