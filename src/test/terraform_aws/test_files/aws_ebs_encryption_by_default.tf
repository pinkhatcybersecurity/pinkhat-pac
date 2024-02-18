resource "aws_ebs_encryption_by_default" "vulnerable" {
  enabled = false
}

resource "unknown_component" "not_vulnerable" {
  enabled = true
}

resource "aws_ebs_encryption_by_default" "not_vulnerable" {
  enabled = true
}
