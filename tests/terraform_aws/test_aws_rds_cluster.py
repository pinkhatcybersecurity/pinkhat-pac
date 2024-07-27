import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.no_cloud_watch",
        "description": "Logging and monitoring is a key aspect of running infrastructure. If there is no proper "
        "logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch:\n- audit\n- error\n- general\n- slowquery\n- "
        "postgresql if engine postgresql\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#enabled_cloudwatch_logs_exports\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Procedural.UploadtoCloudWatch.html\n",
        "remediation": 'Enable sending RDS logs to cloudwach:\nresource "aws_rds_cluster" "rds_cluster" {\n  ...\n  '
        'enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery", "postgresql"]\n}\n',
        "issue": None,
        "line_of_code": 1,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.nothing",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 26,
    },
    {
        "file_path": "tests/terraform_aws/test_files/aws_rds_cluster.tf",
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.nothing",
        "description": "Logging and monitoring is a key aspect of running infrastructure. If there is no proper "
        "logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch:\n- audit\n- error\n- general\n- slowquery\n- "
        "postgresql if engine postgresql\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#enabled_cloudwatch_logs_exports\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Procedural.UploadtoCloudWatch.html\n",
        "remediation": 'Enable sending RDS logs to cloudwach:\nresource "aws_rds_cluster" "rds_cluster" {\n  ...\n  '
        'enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery", "postgresql"]\n}\n',
        "issue": None,
        "line_of_code": 26,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 42,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled",
        "description": "Logging and monitoring is a key aspect of running infrastructure. If there is no proper "
        "logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch:\n- audit\n- error\n- general\n- slowquery\n- "
        "postgresql if engine postgresql\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#enabled_cloudwatch_logs_exports\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Procedural.UploadtoCloudWatch.html\n",
        "remediation": 'Enable sending RDS logs to cloudwach:\nresource "aws_rds_cluster" "rds_cluster" {\n  ...\n  '
        'enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery", "postgresql"]\n}\n',
        "issue": None,
        "line_of_code": 42,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled_all",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 60,
    },
    {
        "file_path": "tests/terraform_aws/test_files/aws_rds_cluster.tf",
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled_all",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#preferred_maintenance_window\n"
        "https://repost.aws/knowledge-center/rds-maintenance-window\n",
        "remediation": 'Provide maintenance window based on your needs\nresource "aws_rds_cluster" '
        '"rds_cluster" {\n  ...\n  preferred_maintenance_window = "Mon:00:00-Mon:03:00"\n}\n',
        "issue": None,
        "line_of_code": 60,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled_mssql_all",
        "description": "By default, AWS RDS have no deletion protection (default value is false). "
        "Please find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#deletion_protection\n"
        "deletion_protection: enables deletion protection for aws_rds_cluster. The defaults is false\n",
        "remediation": "Enable deletion protection by adding deletion_protection_enabled\n"
        'resource "aws_rds_cluster" "rds_cluster" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection_enabled value to true\n",
        "issue": None,
        "line_of_code": 77,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_rds_cluster.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_rds_cluster",
        "graph_name": "aws_rds_cluster.cloud_watch_enabled_mssql_all",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#preferred_maintenance_window\n"
        "https://repost.aws/knowledge-center/rds-maintenance-window\n",
        "remediation": 'Provide maintenance window based on your needs\nresource "aws_rds_cluster" "rds_cluster" '
        '{\n  ...\n  preferred_maintenance_window = "Mon:00:00-Mon:03:00"\n}\n',
        "issue": None,
        "line_of_code": 77,
    },
]


def test_aws_rds_cluster():
    test_file_name = "aws_rds_cluster.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
