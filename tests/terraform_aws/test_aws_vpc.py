import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_vpc.tf"),
        "category": "terraform",
        "rule_name": "Missing flowlogs for VPC",
        "module": "aws_vpc",
        "graph_name": "aws_vpc.missing_flowlogs",
        "description": "Flowlogs captures IP traffic for a specific VPC. Logs can be sent to S3, "
        "CloudWatch or Amazon Kinesis\n",
        "remediation": "",
        "issue": "",
        "line_of_code": 5,
    },
]


def test_aws_vpc():
    test_file_name = "aws_vpc.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
