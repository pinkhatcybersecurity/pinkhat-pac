import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests",
            "terraform_aws",
            "test_files",
            "aws_elasticache_replication_group.tf",
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Transit",
        "module": "aws_elasticache_replication_group",
        "graph_name": "aws_elasticache_replication_group.example",
        "description": "Data send over the internet must be encrypted to protect information from unauthorized "
        "disclosure or modifications. End to end encryption should be used. "
        "TLS is the common cryptographic protocol.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_replication_group#transit_encryption_enabled\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_replication_group.\n"
        'resource "aws_elasticache_replication_group" "elasticache_group" {\n  ...'
        "\n  transit_encryption_enabled = true\n  ...\n}\n",
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests",
            "terraform_aws",
            "test_files",
            "aws_elasticache_replication_group.tf",
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_elasticache_replication_group",
        "graph_name": "aws_elasticache_replication_group.example",
        "description": "Encryption provides protection if the data is stolen, modified or compromised. "
        "The data must protected in:\n- rest - use - and transit\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_replication_group#at_rest_encryption_enabled\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/at-rest-encryption.html\n",
        "remediation": "Enable at_rest_encryption_enabled in aws_elasticache_replication_group.\n"
        'resource "aws_elasticache_replication_group" "elasticache_group" {\n  ...\n'
        "  at_rest_encryption_enabled = true\n  ...\n}\n",
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests",
            "terraform_aws",
            "test_files",
            "aws_elasticache_replication_group.tf",
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Transit",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.replica",
        "description": "Data send over the internet must be encrypted to protect information from unauthorized "
        "disclosure or modifications. End to end encryption should be used. "
        "TLS is the common cryptographic protocol.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_cluster#transit_encryption_enabled\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  transit_encryption_enabled = true\n  ...\n}\n",
        "issue": None,
        "line_of_code": 17,
    },
    {
        "file_path": os.path.join(
            "tests",
            "terraform_aws",
            "test_files",
            "aws_elasticache_replication_group.tf",
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.replica",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_cluster#maintenance_window\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  maintenance_window = 'sun:10:00-sun:11:00'\n  ...\n}\n",
        "issue": None,
        "line_of_code": 17,
    },
]


def test_aws_elasticache_replication_group():
    test_file_name = "aws_elasticache_replication_group.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
