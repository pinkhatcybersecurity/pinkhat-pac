from abc import ABC, abstractmethod

from iacparsers.vulnerability_definition import VulnerabilityDefinition


class TerraformSecurityCheckCore(ABC):
    @classmethod
    @abstractmethod
    def _get_security_checks(cls) -> list:
        raise NotImplementedError()

    @classmethod
    def terraform_resource_parser(
        cls, file_name: str, component: dict
    ) -> list[VulnerabilityDefinition]:
        return [
            vulnerability
            for terraform_resource_name, terraform_resource_values in component.items()
            for security_check in cls._get_security_checks()
            if (
                vulnerability := security_check(
                    file_name=file_name,
                    terraform_resource_name=terraform_resource_name,
                    terraform_resource_values=terraform_resource_values,
                )
            )
            is not None
        ]
