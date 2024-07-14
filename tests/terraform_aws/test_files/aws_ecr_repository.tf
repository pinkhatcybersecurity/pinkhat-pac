resource "aws_ecr_repository" "only_image_scanning" {
  name                 = "only_image_scanning"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "no_image_scanning" {
  name                 = "no_image_scanning"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_repository" "force_delete" {
  name                 = "force_delete"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}
