import os

from tests.core_config import run_test

issues = [
    {
        "file_path": "tests/terraform_aws/test_files/aws_ecr_repository.tf",
        "category": "terraform",
        "rule_name": "ECR Security scanning registry",
        "module": "aws_ecr_repository",
        "graph_name": "aws_ecr_repository.no_image_scanning",
        "description": "The container image might have installed multiple different packages or libraries. "
        "Those libraries might contain identified vulnerabilities i.e. CVEs. "
        "By default, image scanning is manual and user initiated. "
        "It adds unnecessary complexity to the process and might cause that your image won't be never "
        "scanned. It is strongly recommended to enable a flag scan_on_push. "
        "You can get more information in the link below: "
        "https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/"
        "resources/ecr_repository#image_scanning_configuration "
        "scan_on_push: if true, then image is scanned on the push, if false, then not scanned.\n",
        "remediation": "Enable scan_on_push in your terraform code:\n"
        'resource "aws_ecr_repository" "ecr_repository_name" {\n  ...\n  '
        "image_scanning_configuration {\n    scan_on_push = true\n  }\n  ...\n}\n",
        "issue": None,
        "line_of_code": 10,
    },
    {
        "file_path": "tests/terraform_aws/test_files/aws_ecr_repository.tf",
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_ecr_repository",
        "graph_name": "aws_ecr_repository.force_delete",
        "description": "It's possible to delete ECR even if it contains images. "
        "The default option for aws_ecr_repository - force_delete is False "
        "force_delete: if true then deletes the repository with existing data in it\n",
        "remediation": "Disable force_delete option by changing it the value to false\n"
        'resource "aws_ecr_repository" "ecr_repository_name" {\n  ...\n  force_delete = false\n}\n',
        "issue": None,
        "line_of_code": 19,
    },
]


def test_aws_ecr_repository():
    test_file_name = "aws_ecr_repository.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
