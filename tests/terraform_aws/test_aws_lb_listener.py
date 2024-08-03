import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_lb_listener.tf"
        ),
        "category": "terraform",
        "rule_name": "Expired certificate verification for mutual authentication",
        "module": "aws_lb_listener",
        "graph_name": "aws_lb_listener.mutual_authentication_ignore_cert",
        "description": "Expired certificates for mutual authentication might cause very serious cybersecurity issues. "
        "If an application accepts expired certificates, then mostly developers disable verify "
        "certificate parameter. It impacts trust between systems and there is ability for man in "
        "the middle attacks (MITM).\nignore_client_certificate_expiry - if true bypass expiry date. "
        "Default value is false\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener#mutual_authentication\n",
        "remediation": "Disable or remove ignore_client_certificate_expiry in aws_lb_listener resource.\n",
        "issue": None,
        "line_of_code": 7,
    }
]


def test_aws_lb_listener():
    test_file_name = "aws_lb_listener.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
