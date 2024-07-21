import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_vpc.tf"),
        "category": "terraform",
        "rule_name": "Missing flowlogs for VPC",
        "module": "aws_vpc",
        "graph_name": "aws_vpc.missing_flowlogs",
        "description": "It's really important to get information about IP traffic in VPC. "
        "If there is no enough logging information then it's impossible to track system communication "
        "and spot if there is something wrong. It is really important in case of security incident. "
        "Flowlogs captures IP traffic for a specific VPC. Logs can be sent to S3, CloudWatch or Amazon Kinesis\n",
        "remediation": 'Consider adding Flowlogs to VPC:\nresource "aws_vpc" "flowlogs_enabled" '
        '{\n  cidr_block = "127.0.0.1/16"\n}\nresource "aws_flow_log" "flowlog_exist" '
        '{\n  traffic_type    = "ALL"\n  vpc_id          = aws_vpc.flowlogs_enabled.id\n}\n',
        "issue": None,
        "line_of_code": 5,
    }
]


def test_aws_vpc():
    test_file_name = "aws_vpc.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
