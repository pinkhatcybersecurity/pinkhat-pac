from dataclasses import dataclass


@dataclass
class IssueDefinition:
    file_path: str
    category: str
    rule_name: str
    module: str
    graph_name: str
    description: str
    remediation: str
    issue: str
    line_of_code: int
