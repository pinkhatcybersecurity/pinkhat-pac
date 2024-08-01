import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.vulnerable_default",
        "description": "Encryption provides protection if the data is stolen, "
        "modified or compromised. The data must protected in:\n- rest\n- use\n- and transit\nT"
        "he default value of storage_encrypted is False.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#storage_encrypted\n",
        "remediation": 'Enable encryption in DB Instance:\n\'\'\' resource "aws_db_instance" "db_instance" {\n'
        "  ...\n  storage_encrypted  = true\n} '''\n",
        "issue": None,
        "line_of_code": 13,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.vulnerable_default",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window. "
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
        "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "Provide maintenance window based on your needs\n"
        'resource "aws_db_instance" "db_instance_name" '
        '{\n  ...\n  maintenance_window          = "Mon:00:00-Mon:03:00"\n}\n',
        "issue": None,
        "line_of_code": 13,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Publicly accessible database",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.vulnerable_default",
        "description": "Publicly accessible database might lead to data leakage through:\n\n"
        "  - security vulnerability in the database\n"
        "  - default user name and password\n"
        "  - weak passwords\n"
        "  - and more\n\n"
        "Database should be hidden and not accessible via internet.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#publicly_accessible\n"
        "publicly_accessible - default value is false\n",
        "remediation": "Disable publicly_accessible in aws_db_instance\n"
        'resource "aws_db_instance" "db_instance_name" {\n  ...\n  publicly_accessible = false\n}\n',
        "issue": None,
        "line_of_code": 13,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.vulnerable_default",
        "description": "By default, AWS DB Instance have no database deletion protection (default value is false). "
        "Please find more information in the below link: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#deletion_protection\n"
        "deletion_protection: enables deletion protection for DB instance. Defaults to false\n",
        "remediation": "Enable deletion protection by adding deletion_protection\n"
        'resource "aws_db_instance" "db_instance_name" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection value to true\n",
        "issue": None,
        "line_of_code": 13,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.vulnerable_default",
        "description": "Logging and monitoring is a key aspect of running infrastructure. "
        "If there is no proper logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch:\n- audit\n- error\n- general\n- slowquery\n- "
        "postgresql if engine postgresql\nThe following values are valid for each DB engine:\n"
        "- RDS for Db2 - diag.log | notify.log\n"
        "- RDS for MariaDB - audit | error | general | slowquery\n"
        "- RDS for Microsoft SQL Server - agent | error\n"
        "- RDS for MySQL - audit | error | general | slowquery\n"
        "- RDS for Oracle - alert | audit | listener | trace | oemagent\n"
        "- RDS for PostgreSQL - postgresql | upgrade\n\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#enabled_cloudwatch_logs_exports\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Procedural.UploadtoCloudWatch.html\n",
        "remediation": 'Enable sending DB instance logs to cloudwach:\nresource "aws_db_instance" "db_instance" {'
        '\n  ...\n  engine = "sqlserver-ex"\n  enabled_cloudwatch_logs_exports = ["agent", "error"]\n}\n',
        "issue": None,
        "line_of_code": 13,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.test-replica",
        "description": "By default, AWS DB Instance have no database deletion protection (default value is false). "
        "Please find more information in the below link: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#deletion_protection\n"
        "deletion_protection: enables deletion protection for DB instance. Defaults to false\n",
        "remediation": "Enable deletion protection by adding deletion_protection\n"
        'resource "aws_db_instance" "db_instance_name" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection value to true\n",
        "issue": None,
        "line_of_code": 39,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Audit Log Management",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.test-replica",
        "description": "Logging and monitoring is a key aspect of running infrastructure. "
        "If there is no proper logging then some events or malicious actions might be missed. "
        "The below actions can be send to cloudwatch:\n- audit\n- error\n- general\n- slowquery\n- "
        "postgresql if engine postgresql\nThe following values are valid for each DB engine:\n"
        "- RDS for Db2 - diag.log | notify.log\n"
        "- RDS for MariaDB - audit | error | general | slowquery\n"
        "- RDS for Microsoft SQL Server - agent | error\n"
        "- RDS for MySQL - audit | error | general | slowquery\n"
        "- RDS for Oracle - alert | audit | listener | trace | oemagent\n"
        "- RDS for PostgreSQL - postgresql | upgrade\n\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#enabled_cloudwatch_logs_exports\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html\n"
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Procedural.UploadtoCloudWatch.html\n",
        "remediation": 'Enable sending DB instance logs to cloudwach:\nresource "aws_db_instance" "db_instance" {'
        '\n  ...\n  engine = "sqlserver-ex"\n  enabled_cloudwatch_logs_exports = ["agent", "error"]\n}\n',
        "issue": None,
        "line_of_code": 39,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Encrypt Sensitive Data at Rest",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.secret_manager",
        "description": "Encryption provides protection if the data is stolen, "
        "modified or compromised. The data must protected in:\n- rest\n- use\n- and transit\nT"
        "he default value of storage_encrypted is False.\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#storage_encrypted\n",
        "remediation": 'Enable encryption in DB Instance:\n\'\'\' resource "aws_db_instance" "db_instance" {\n'
        "  ...\n  storage_encrypted  = true\n} '''\n",
        "issue": None,
        "line_of_code": 78,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.secret_manager",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
        "The required work must be implemented during the maintenance window. "
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
        "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": "Provide maintenance window based on your needs\n"
        'resource "aws_db_instance" "db_instance_name" '
        '{\n  ...\n  maintenance_window          = "Mon:00:00-Mon:03:00"\n}\n',
        "issue": None,
        "line_of_code": 78,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Backup retention policy",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.secret_manager",
        "description": "Data recovery is a key aspect for the application availability. "
        "Backup retention period in aws_db_instance defines for how long backup is stored. "
        "The value is between 0 and 35 days. You can find more information in the link below:\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/"
        "db_instance#backup_retention_period\n",
        "remediation": "Create a backup retention policy for aws_db_instance greater than 0\n"
        'resource "aws_db_instance" "db_instance_name" {\n  ...\n  backup_retention_period = 1\n}\n',
        "issue": None,
        "line_of_code": 78,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_db_instance.tf"
        ),
        "category": "terraform",
        "rule_name": "Enable Deletion Protection",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.secret_manager",
        "description": "By default, AWS DB Instance have no database deletion protection (default value is false). "
        "Please find more information in the below link: "
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance#deletion_protection\n"
        "deletion_protection: enables deletion protection for DB instance. Defaults to false\n",
        "remediation": "Enable deletion protection by adding deletion_protection\n"
        'resource "aws_db_instance" "db_instance_name" '
        "{\n  ...\n  deletion_protection = true\n} or changing deletion_protection value to true\n",
        "issue": None,
        "line_of_code": 78,
    },
]


def test_aws_db_instance():
    test_file_name = "aws_db_instance.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
