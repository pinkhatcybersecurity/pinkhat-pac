import os

from tests.core_config import run_test

issues = [
    {
        "file_path": "tests/terraform_aws/test_files/aws_ecr_repository.tf",
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_ecr_repository",
        "graph_name": "aws_ecr_repository.force_delete",
        "description": "It's possible to delete ECR even if it contains images. "
                       "The default option for aws_ecr_repository - force_delete is False "
                       "force_delete: if true then deletes the repository with existing data in it\n",
        "remediation": 'Disable force_delete option by changing it the value to false\n'
                       'resource "aws_ecr_repository" "ecr_repository_name" {\n  ...\n  force_delete = false\n}\n',
        "issue": None,
        "line_of_code": 19,
    }
]


def test_aws_ecr_repository():
    test_file_name = "aws_ecr_repository.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
