from abc import ABC, abstractmethod

from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TFSecurityCheckCore(ABC):
    @classmethod
    @abstractmethod
    def _get_sec_checks(cls) -> list:
        raise NotImplementedError()

    @classmethod
    def terraform_resource_parser(
        cls, file_name: str, component: dict
    ) -> list[VulnerabilityDefinition]:
        return [
            vulnerability
            for tf_resource_name, tf_resource_values in component.items()
            for security_check in cls._get_sec_checks()
            if (
                vulnerability := security_check(
                    file_name=file_name,
                    tf_resource_name=tf_resource_name,
                    tf_resource_values=tf_resource_values,
                )
            )
            is not None
        ]
