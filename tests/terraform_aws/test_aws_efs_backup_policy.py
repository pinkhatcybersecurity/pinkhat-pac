import os

from tests.core_config import run_test

issues = [
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_efs_backup_policy.tf"
        ),
        "category": "terraform",
        "rule_name": "Backup policy exists for EFS file system",
        "module": "aws_efs_file_system",
        "graph_name": "aws_efs_file_system.backup_disabled",
        "description": "If there is no backup for EFS policy. It might cause a serious issue in a case of disaster. "
        "Please find more information in the below links:\n"
        "https://docs.aws.amazon.com/efs/latest/ug/API_BackupPolicy.html\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/efs_backup_policy#backup_policy\n",
        "remediation": "Add backup policy for EFS file system: ''' resource \"aws_efs_backup_policy\" "
        '"policy" {\n  file_system_id = aws_efs_file_system.happy_file_system.id\n\n  '
        "backup_policy {\n    status = \"ENABLED\"\n  }\n} '''\n",
        "issue": None,
        "line_of_code": 14,
    },
    {
        "file_path": os.path.join(
            "tests", "terraform_aws", "test_files", "aws_efs_backup_policy.tf"
        ),
        "category": "terraform",
        "rule_name": "Data Recovery",
        "module": "aws_efs_backup_policy",
        "graph_name": "aws_efs_backup_policy.policy_backup_disabled",
        "description": "If there is no backup for EFS policy. It might cause a serious issue in a case of disaster. "
        "Please find more information in the below links:\n"
        "https://docs.aws.amazon.com/efs/latest/ug/API_BackupPolicy.html\n"
        "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/efs_backup_policy#backup_policy\n",
        "remediation": "Add backup policy for EFS file system: ''' resource \"aws_efs_backup_policy\" "
        '"policy" {\n  file_system_id = aws_efs_file_system.happy_file_system.id\n\n  '
        "backup_policy {\n    status = \"ENABLED\"\n  }\n} '''\n",
        "issue": None,
        "line_of_code": 19,
    },
]


def test_aws_efs_backup_policy():
    test_file_name = "aws_efs_backup_policy.tf"
    test_file_path = os.path.join(
        "tests", "terraform_aws", "test_files", test_file_name
    )
    run_test(test_file_path=test_file_path, issues=issues)
