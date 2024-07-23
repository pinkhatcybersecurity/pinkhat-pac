import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_efs_file_system.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_efs_file_system",
        "graph_name": "aws_efs_file_system.no_encryption_and_data_classification",
        "description": "Encryption provides protection if the data is stolen, modified or compromised. "
        "The data must protected in: - rest - use - and transit CIS 2.4.1 Ensure that encryption is "
        "enabled for EFS file systems. Description of *aws_efs_file_system* terraform module: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/efs_file_system#encrypted\n",
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": "",
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_efs_file_system.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_efs_file_system",
        "graph_name": "aws_efs_file_system.happy_file_system",
        "description": "Encryption provides protection if the data is stolen, modified or compromised. "
        "The data must protected in: - rest - use - and transit "
        "CIS 2.4.1 Ensure that encryption is enabled for EFS file systems. "
        "Description of *aws_efs_file_system* terraform module: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/efs_file_system#encrypted\n",
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": "",
        "line_of_code": 9,
    },
]


def test_aws_efs_file_system():
    test_file_name = "aws_efs_file_system.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
