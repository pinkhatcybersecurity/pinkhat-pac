import os
from pathlib import Path

from loguru import logger

from iacparsers.terraform_core import TerraformCore
from iacparsers.vulnerability_definition import VulnerabilityDefinition
from iacparsers.yaml_files import YamlFile


class CoreScanning:
    SCANNERS = [YamlFile, TerraformCore]
    results: list[VulnerabilityDefinition] = []

    def start_scanning(self, path: str) -> None:
        for child in Path(path).rglob("*.*"):
            file_path = os.path.join(path, child.name)
            if child.is_file():
                logger.info(f"Parsing {file_path}")
                file_extension = file_path[file_path.rfind(".") :]
                for scanner in self.SCANNERS:
                    if file_extension in scanner.FILE_EXTENSION:
                        self.results += scanner.run_scan(
                            file_name=file_path, content=child.read_text()
                        )
            else:
                self.start_scanning(path=file_path)

    def get_vulnerabilities(self) -> list[VulnerabilityDefinition]:
        return self.results

    def get_vulnerabilities_dict(self) -> list[dict]:
        return [result.__dict__ for result in self.results]
