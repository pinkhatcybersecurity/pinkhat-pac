import yaml
from loguru import logger

from iacparsers.ansible.builtin.ansible_builtin_copy import AnsibleBuiltinCopy
from iacparsers.ansible.builtin.ansible_builtin_file import AnsibleBuiltinFile
from iacparsers.utils.yaml_safe_line_loader import SafeLineLoader


class YamlFile:
    FILE_EXTENSION = [".yaml", ".yml"]
    iac_modules = {
        AnsibleBuiltinCopy.MODULE_NAME: lambda file_name, component: AnsibleBuiltinCopy.ansible_resource_parser(
            file_name=file_name, component=component
        ),
        AnsibleBuiltinFile.MODULE_NAME: lambda file_name, component: AnsibleBuiltinFile.ansible_resource_parser(
            file_name=file_name, component=component
        ),
    }
    only_iac_modules_names = set(iac_modules.keys())

    @staticmethod
    def run_scan(file_name: str, content: str):
        results = []
        file_extension = file_name[file_name.rfind(".") :]
        if file_extension not in YamlFile.FILE_EXTENSION:
            return results
        resources = yaml.load(content, Loader=SafeLineLoader)
        resource: dict
        for resource in resources:
            component: dict
            results += YamlFile._parse_ansible_resource(
                file_name=file_name, resource=resource
            )
        return results

    @staticmethod
    def _parse_ansible_resource(file_name: str, resource: dict):
        results = []
        for module, component in resource.items():
            if module not in YamlFile.only_iac_modules_names:
                continue
            ansible_resource_parser = YamlFile.iac_modules.get(module)
            if not ansible_resource_parser:
                logger.critical(f"There is no method for {ansible_resource_parser}")
                continue
            results += ansible_resource_parser(file_name=file_name, component=resource)
        return results
