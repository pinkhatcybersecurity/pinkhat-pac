import os

from tests.core_config import run_test

issues = [
    {
        "file_path": "tests/terraform_aws/test_files/aws_dynamodb_table.tf",
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_dynamodb_table",
        "graph_name": "aws_dynamodb_table.dynamodb_vulnerable",
        "description": "By default, AWS Dynamo Tables have no table deletion protection (default value is false). "
        "Please find more information in the below link: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "dynamodb_table#deletion_protection_enabled\n"
        "deletion_protection_enabled: enables deletion protection for table. Defaults to false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_dynamodb_table" "dynamo_table_name" '
        "{\n  ...\n  deletion_protection_enabled = true\n} "
        "or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": "tests/terraform_aws/test_files/aws_dynamodb_table.tf",
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_dynamodb_table",
        "graph_name": "aws_dynamodb_table.dynamodb_vulnerable_without_server_side_encryption",
        "description": "By default, AWS Dynamo Tables have no table deletion protection (default value is false). "
        "Please find more information in the below link: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/"
        "resources/dynamodb_table#deletion_protection_enabled\n"
        "deletion_protection_enabled: enables deletion protection for table. Defaults to false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_dynamodb_table" "dynamo_table_name" '
        "{\n  ...\n  deletion_protection_enabled = true\n} "
        "or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 26,
    },
]


def test_resource_aws_dynamodb_table():
    test_file_name = "aws_dynamodb_table.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
