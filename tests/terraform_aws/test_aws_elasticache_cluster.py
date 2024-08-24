import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.transit_enabled",
        "description": "More information about maintenance window from AWS: "
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
        "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "",
        "issue": "",
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.transit_enabled",
        "description": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Log_Delivery.html",
        "remediation": "",
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Transit",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.no_encryption_in_transit",
        "description": "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "",
        "issue": "",
        "line_of_code": 11,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.no_encryption_in_transit",
        "description": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Log_Delivery.html",
        "remediation": "",
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
        "description": "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "",
        "issue": "",
        "line_of_code": 21,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.contains_both_log_delivery_configuration",
        "description": "More information about maintenance window from AWS: "
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
        "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "",
        "issue": "",
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
        "description": "https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/in-transit-encryption.html\n",
        "remediation": "",
        "issue": "",
        "line_of_code": 42,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.onlyfirehose",
        "description": "More information about maintenance window from AWS: "
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
        "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "",
        "issue": "",
        "line_of_code": 42,
    },
]


def test_resource_aws_elasticache_cluster():
    test_file_name = "aws_elasticache_cluster.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
