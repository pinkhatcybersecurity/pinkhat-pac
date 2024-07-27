resource "aws_efs_file_system" "backup_enabled" {
  creation_token = "abc"
  encrypted = true
}

resource "aws_efs_backup_policy" "policy_backup_enabled" {
  file_system_id = aws_efs_file_system.backup_enabled.id

  backup_policy {
    status = "ENABLED"
  }
}

resource "aws_efs_file_system" "backup_disabled" {
  creation_token = "abc"
  encrypted = true
}

resource "aws_efs_backup_policy" "policy_backup_disabled" {
  file_system_id = aws_efs_file_system.backup_disabled.id

  backup_policy {
    status = "DISABLED"
  }
}
