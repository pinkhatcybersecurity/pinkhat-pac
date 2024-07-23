resource "aws_efs_file_system" "no_encryption_and_data_classification" {
  creation_token = "my-product"

  tags = {
    Name = "MyProduct"
  }
}

resource "aws_efs_file_system" "happy_file_system" {
  creation_token = "happy_efs_file_system"
}

resource "aws_efs_backup_policy" "policy" {
  file_system_id = aws_efs_file_system.happy_file_system.id

  backup_policy {
    status = "ENABLED"
  }
}
