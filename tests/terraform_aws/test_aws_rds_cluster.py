import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.nothing",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 26,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 42,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled_all",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 60,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled_mssql_all",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 77,
    },
]


def test_aws_rds_cluster():
    test_file_name = "aws_rds_cluster.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
