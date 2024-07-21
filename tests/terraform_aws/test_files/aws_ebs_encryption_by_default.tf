resource "aws_ebs_encryption_by_default" "vulnerable" {
  enabled = false
}

resource "aws_ebs_encryption_by_default" "not_vulnerable" {
  enabled = true
}
