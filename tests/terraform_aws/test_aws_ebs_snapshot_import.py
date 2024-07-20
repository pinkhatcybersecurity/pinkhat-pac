import os.path

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_ebs_snapshot_import.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_ebs_snapshot_import",
        "graph_name": "aws_ebs_snapshot_import.vulnerable",
        "description": (
            "CIS Control 2.2.1 Ensure EBS volume encryption is enabled."
            " Description of *aws_ebs_snapshot_import* terraform module:"
            " https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_import\n"
        ),
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": None,
        "line_of_code": 18,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_ebs_snapshot_import.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_ebs_snapshot_import",
        "graph_name": "aws_ebs_snapshot_import.vulnerable_false",
        "description": (
            "CIS Control 2.2.1 Ensure EBS volume encryption is enabled."
            " Description of *aws_ebs_snapshot_import* terraform module:"
            " https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_import\n"
        ),
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": None,
        "line_of_code": 34,
    },
]


def test_resource_aws_ebs_snapshot_import():
    test_file_name = "aws_ebs_snapshot_import.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
