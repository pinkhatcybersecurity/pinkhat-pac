import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Transit",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.no_encryption_in_transit",
        "description": "Data send over the internet must be encrypted to protect information from "
        "unauthorized disclosure or modifications. End to end encryption should be used. "
        "TLS is the common cryptographic protocol.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#"
        "transit_encryption_enabled\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  transit_encryption_enabled = true\n  ...\n}\n",
        "issue": None,
        "line_of_code": 11,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Transit",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.contains_both_log_delivery_configuration",
        "description": "Data send over the internet must be encrypted to protect information from "
        "unauthorized disclosure or modifications. End to end encryption should be used. "
        "TLS is the common cryptographic protocol.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#"
        "transit_encryption_enabled\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  transit_encryption_enabled = true\n  ...\n}\n",
        "issue": None,
        "line_of_code": 21,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Transit",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.onlyfirehose",
        "description": "Data send over the internet must be encrypted to protect information from "
        "unauthorized disclosure or modifications. End to end encryption should be used. "
        "TLS is the common cryptographic protocol.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#"
        "transit_encryption_enabled\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  transit_encryption_enabled = true\n  ...\n}\n",
        "issue": None,
        "line_of_code": 42,
    },
]


def test_resource_aws_elasticache_cluster():
    test_file_name = "aws_elasticache_cluster.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
