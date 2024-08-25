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
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_cluster#maintenance_window\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  maintenance_window = 'sun:10:00-sun:11:00'\n  ...\n}\n",
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": "tests/terraform_aws/test_files/aws_elasticache_cluster.tf",
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_elasticache_cluster",
        "graph_name": None,
        "description": "Logging and monitoring is a key aspect of running infrastructure. "
        "If there is no proper logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch or kinesis:\n- slow-log\n- engine-log\n"
        "The feature is available only for Redis\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#log_delivery_configuration\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#log-delivery-configuration\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Log_Delivery.html\n",
        "remediation": "Enable sending slow and engine logs to Cloudwatch or Kinesis\n\n"
        'resource "aws_elasticache_cluster" "elasticache" {\n  ...\n  engine            = "redis"\n'
        "  ...\n  log_delivery_configuration {\n    destination      = aws_cloudwatch_log_group.example.name\n"
        '    destination_type = "cloudwatch-logs"\n    log_format       = "text"\n'
        '    log_type         = "slow-log"\n  }\n'
        "  log_delivery_configuration {\n    destination      = aws_kinesis_firehose_delivery_stream.example.name\n"
        '    destination_type = "kinesis-firehose"\n    log_format       = "json"\n'
        '    log_type         = "engine-log"\n  }\n}\n',
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
        "file_path": "tests/terraform_aws/test_files/aws_elasticache_cluster.tf",
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_elasticache_cluster",
        "graph_name": None,
        "description": "Logging and monitoring is a key aspect of running infrastructure. "
        "If there is no proper logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch or kinesis:\n- slow-log\n- engine-log\n"
        "The feature is available only for Redis\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#log_delivery_configuration\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#log-delivery-configuration\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Log_Delivery.html\n",
        "remediation": "Enable sending slow and engine logs to Cloudwatch or Kinesis\n\n"
        'resource "aws_elasticache_cluster" "elasticache" {\n  ...\n  engine            = "redis"\n'
        "  ...\n  log_delivery_configuration {\n    destination      = aws_cloudwatch_log_group.example.name\n"
        '    destination_type = "cloudwatch-logs"\n    log_format       = "text"\n'
        '    log_type         = "slow-log"\n  }\n'
        "  log_delivery_configuration {\n    destination      = aws_kinesis_firehose_delivery_stream.example.name\n"
        '    destination_type = "kinesis-firehose"\n    log_format       = "json"\n'
        '    log_type         = "engine-log"\n  }\n}\n',
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
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.contains_both_log_delivery_configuration",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_cluster#maintenance_window\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  maintenance_window = 'sun:10:00-sun:11:00'\n  ...\n}\n",
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
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_elasticache_cluster",
        "graph_name": "aws_elasticache_cluster.onlyfirehose",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "elasticache_cluster#maintenance_window\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "Enable transit_encryption_enabled in aws_elasticache_cluster.\n"
        'resource "aws_elasticache_cluster" "elasticache_cluster" {\n  ...\n'
        "  maintenance_window = 'sun:10:00-sun:11:00'\n  ...\n}\n",
        "issue": None,
        "line_of_code": 42,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_elasticache_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_elasticache_cluster",
        "graph_name": None,
        "description": "Logging and monitoring is a key aspect of running infrastructure. "
        "If there is no proper logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch or kinesis:\n- slow-log\n- engine-log\n"
        "The feature is available only for Redis\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#log_delivery_configuration\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_cluster#log-delivery-configuration\n"
        "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Log_Delivery.html\n",
        "remediation": "Enable sending slow and engine logs to Cloudwatch or Kinesis\n\n"
        'resource "aws_elasticache_cluster" "elasticache" {\n  ...\n  engine            = "redis"\n'
        "  ...\n  log_delivery_configuration {\n    destination      = aws_cloudwatch_log_group.example.name\n"
        '    destination_type = "cloudwatch-logs"\n    log_format       = "text"\n'
        '    log_type         = "slow-log"\n  }\n'
        "  log_delivery_configuration {\n    destination      = aws_kinesis_firehose_delivery_stream.example.name\n"
        '    destination_type = "kinesis-firehose"\n    log_format       = "json"\n'
        '    log_type         = "engine-log"\n  }\n}\n',
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
