import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_lb",
        "graph_name": "aws_lb.missing_enable_deletion_protection",
        "description": "By default, AWS LB Instance have no deletion protection (default value is false). "
        "The resource might be accidentally deleted and cause damage. "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#enable_deletion_protection\n",
        "remediation": "Enable delete protection by setting enable_deletion_protection to true in aws_lb. Defaults to false\n"
        'resource "aws_lb" "test" {\n  ...\n  enable_deletion_protection = true\n  ...\n}\n',
        "issue": None,
        "line_of_code": 22,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_false",
        "description": "By default, AWS LB Instance have no deletion protection (default value is false). "
        "The resource might be accidentally deleted and cause damage. "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#enable_deletion_protection\n",
        "remediation": "Enable delete protection by setting enable_deletion_protection to true in aws_lb. Defaults to false\n"
        'resource "aws_lb" "test" {\n  ...\n  enable_deletion_protection = true\n  ...\n}\n',
        "issue": None,
        "line_of_code": 41,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_missing",
        "description": "By default, AWS LB Instance have no deletion protection (default value is false). "
        "The resource might be accidentally deleted and cause damage. "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#enable_deletion_protection\n",
        "remediation": "Enable delete protection by setting enable_deletion_protection to true in aws_lb. Defaults to false\n"
        'resource "aws_lb" "test" {\n  ...\n  enable_deletion_protection = true\n  ...\n}\n',
        "issue": None,
        "line_of_code": 59,
    },
]


def test_aws_lb():
    test_file_name = "aws_lb.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
