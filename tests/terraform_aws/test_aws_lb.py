import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Disabled Connection Logs for Application Load Balancer",
        "module": "aws_lb",
        "graph_name": "aws_lb.test",
        "description": "Enabling connection logs for Elastic Load Balancing provides information about request received"
        " by load balancer. Log entries contains information about:\n- date time\n- client IP address\n"
        "- client port\n- listener port\n- TLS cipher and protocol used\n- connection status\n"
        "- client certificate details\nAccess logs are very important to analyze traffic and troubleshoot"
        " connectivity issues. load_balancer_type: if 'application' type, then enabled flag should be set "
        'to True in connection_logs. Default option is False"\n'
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#connection_logs\n"
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-connection-logs.html\n",
        "remediation": 'Enable access logs in aws_lb.\nresource "aws_lb" "lb" {\n  ...\n  connection_logs {\n'
        '    bucket  = aws_s3_bucket.lb_logs.id\n    prefix  = "test-lb"\n    enabled = true\n  }\n  ...\n}\n',
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_lb",
        "graph_name": "aws_lb.missing_enable_deletion_protection",
        "description": "By default, AWS LB Instance have no deletion protection (default value is false). "
        "The resource might be accidentally deleted and cause damage. "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#enable_deletion_protection\n",
        "remediation": "Enable delete protection by setting enable_deletion_protection to true in aws_lb. Defaults to false\n"
        'resource "aws_lb" "test" {\n  ...\n  enable_deletion_protection = true\n  ...\n}\n',
        "issue": None,
        "line_of_code": 22,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Disabled Connection Logs for Application Load Balancer",
        "module": "aws_lb",
        "graph_name": "aws_lb.missing_enable_deletion_protection",
        "description": "Enabling connection logs for Elastic Load Balancing provides information about request received"
        " by load balancer. Log entries contains information about:\n- date time\n- client IP address\n"
        "- client port\n- listener port\n- TLS cipher and protocol used\n- connection status\n"
        "- client certificate details\nAccess logs are very important to analyze traffic and troubleshoot"
        " connectivity issues. load_balancer_type: if 'application' type, then enabled flag should be set "
        'to True in connection_logs. Default option is False"\n'
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#connection_logs\n"
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-connection-logs.html\n",
        "remediation": 'Enable access logs in aws_lb.\nresource "aws_lb" "lb" {\n  ...\n  connection_logs {\n'
        '    bucket  = aws_s3_bucket.lb_logs.id\n    prefix  = "test-lb"\n    enabled = true\n  }\n  ...\n}\n',
        "issue": None,
        "line_of_code": 22,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_false",
        "description": "By default, AWS LB Instance have no deletion protection (default value is false). "
        "The resource might be accidentally deleted and cause damage. "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#enable_deletion_protection\n",
        "remediation": "Enable delete protection by setting enable_deletion_protection to true in aws_lb. Defaults to false\n"
        'resource "aws_lb" "test" {\n  ...\n  enable_deletion_protection = true\n  ...\n}\n',
        "issue": None,
        "line_of_code": 41,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Disabled Access Logs for Application Load Balancer",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_false",
        "description": "Enabling access logs for Elastic Load Balancing provides information about request received "
        "by load balancer. Log entries contains information about:\n- date time\n"
        "- client IP address\n- request paths\n- server responses\n"
        "Access logs are very important to analyze traffic and troubleshoot connectivity issues.\n"
        "load_balancer_type: if 'application' type, then enabled flag should be set to True "
        'in access_logs. Default option is False"\n'
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#access_logs\n"
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html\n",
        "remediation": 'Enable access logs in aws_lb.\n\nresource "aws_lb" "lb" {\n  ...\n  access_logs {\n'
        '    bucket  = aws_s3_bucket.lb_logs.id\n    prefix  = "test-lb"\n    enabled = true\n  }\n  ...\n}\n',
        "issue": None,
        "line_of_code": 41,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Disabled Connection Logs for Application Load Balancer",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_false",
        "description": "Enabling connection logs for Elastic Load Balancing provides information about request received"
        " by load balancer. Log entries contains information about:\n- date time\n- client IP address\n"
        "- client port\n- listener port\n- TLS cipher and protocol used\n- connection status\n"
        "- client certificate details\nAccess logs are very important to analyze traffic and troubleshoot"
        " connectivity issues. load_balancer_type: if 'application' type, then enabled flag should be set "
        'to True in connection_logs. Default option is False"\n'
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#connection_logs\n"
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-connection-logs.html\n",
        "remediation": 'Enable access logs in aws_lb.\nresource "aws_lb" "lb" {\n  ...\n  connection_logs {\n'
        '    bucket  = aws_s3_bucket.lb_logs.id\n    prefix  = "test-lb"\n    enabled = true\n  }\n  ...\n}\n',
        "issue": None,
        "line_of_code": 41,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_missing",
        "description": "By default, AWS LB Instance have no deletion protection (default value is false). "
        "The resource might be accidentally deleted and cause damage. "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#enable_deletion_protection\n",
        "remediation": "Enable delete protection by setting enable_deletion_protection to true in aws_lb. Defaults to false\n"
        'resource "aws_lb" "test" {\n  ...\n  enable_deletion_protection = true\n  ...\n}\n',
        "issue": None,
        "line_of_code": 59,
    },
    {
        "file_path": os.path.join("tests", "terraform_aws", "test_files", "aws_lb.tf"),
        "category": "terraform",
        "rule_name": "Disabled Access Logs for Application Load Balancer",
        "module": "aws_lb",
        "graph_name": "aws_lb.access_logs_missing",
        "description": "Enabling access logs for Elastic Load Balancing provides information about request received "
        "by load balancer. Log entries contains information about:\n- date time\n"
        "- client IP address\n- request paths\n- server responses\n"
        "Access logs are very important to analyze traffic and troubleshoot connectivity issues.\n"
        "load_balancer_type: if 'application' type, then enabled flag should be set to True "
        'in access_logs. Default option is False"\n'
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb#access_logs\n"
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html\n",
        "remediation": 'Enable access logs in aws_lb.\n\nresource "aws_lb" "lb" {\n  ...\n  access_logs {\n'
        '    bucket  = aws_s3_bucket.lb_logs.id\n    prefix  = "test-lb"\n    enabled = true\n  }\n  ...\n}\n',
        "issue": None,
        "line_of_code": 59,
    },
]


def test_aws_lb():
    test_file_name = "aws_lb.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
