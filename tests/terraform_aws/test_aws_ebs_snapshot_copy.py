import os.path

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_ebs_snapshot_copy.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_ebs_volume",
        "graph_name": "aws_ebs_volume.simple_volume",
        "description": "CIS Control 2.2.1 Ensure EBS volume encryption is enabled."
        " Description of *aws_ebs_volume* terraform module:"
        " https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_volume\n",
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_ebs_snapshot_copy.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_ebs_snapshot_copy",
        "graph_name": "aws_ebs_snapshot_copy.vulnerable",
        "description": (
            "CIS Control 2.2.1 Ensure EBS volume encryption is enabled."
            " Description of *aws_ebs_snapshot_copy* terraform module:"
            " https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_copy\n"
        ),
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": None,
        "line_of_code": 18,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_ebs_snapshot_copy.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_ebs_snapshot_copy",
        "graph_name": "aws_ebs_snapshot_copy.vulnerable_false",
        "description": (
            "CIS Control 2.2.1 Ensure EBS volume encryption is enabled."
            " Description of *aws_ebs_snapshot_copy* terraform module:"
            " https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ebs_snapshot_copy\n"
        ),
        "remediation": "encrypted: should be set to True. Default option is False",
        "issue": None,
        "line_of_code": 37,
    },
]


def test_resource_aws_ebs_snapshot_copy():
    test_file_name = "aws_ebs_snapshot_copy.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
