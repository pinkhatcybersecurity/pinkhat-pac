import os

from tests.core_config import run_test

issues = [
    {
        "file_path": "tests/terraform_aws/test_files/aws_db_instance.tf",
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.vulnerable_default",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
                       "The required work must be implemented during the maintenance window. "
                       "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
                       "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": 'Provide maintenance window based on your needs\n'
                       'resource "aws_db_instance" "db_instance_name" '
                       '{\n  ...\n  maintenance_window          = "Mon:00:00-Mon:03:00"\n}\n',
        "issue": None,
        "line_of_code": 13,
    },
    {
        "file_path": "tests/terraform_aws/test_files/aws_db_instance.tf",
        "category": "terraform",
        "rule_name": "Maintenance Window for OS patching",
        "module": "aws_db_instance",
        "graph_name": "aws_db_instance.secret_manager",
        "description": "Not all patches and security fixes are automatically implemented in a database. "
                       "The required work must be implemented during the maintenance window. "
                       "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"
                       "USER_UpgradeDBInstance.Maintenance.html#OS_Updates\n",
        "remediation": 'Provide maintenance window based on your needs\n'
                       'resource "aws_db_instance" "db_instance_name" '
                       '{\n  ...\n  maintenance_window          = "Mon:00:00-Mon:03:00"\n}\n',
        "issue": None,
        "line_of_code": 77,
    },
]


def test_aws_db_instance():
    test_file_name = "aws_db_instance.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
