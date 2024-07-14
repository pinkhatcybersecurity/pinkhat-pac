resource "aws_dynamodb_table" "dynamodb_vulnerable" {
  name             = "payment"
  hash_key         = "TestTableHashKey"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  server_side_encryption {
    enabled = false
  }

  attribute {
    name = "TestTableHashKey"
    type = "S"
  }

  replica {
    region_name = "us-east-2"
  }

  replica {
    region_name = "us-west-2"
  }
}

resource "aws_dynamodb_table" "dynamodb_vulnerable_without_server_side_encryption" {
  name             = "users"
  hash_key         = "TestTableHashKey"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "TestTableHashKey"
    type = "S"
  }

  replica {
    region_name = "us-east-2"
  }

  replica {
    region_name = "us-west-2"
  }
}

resource "aws_dynamodb_table" "dynamodb_vulnerable_with_server_side_encryption" {
  name             = "cars"
  hash_key         = "TestTableHashKey"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  deletion_protection_enabled = true

  server_side_encryption {
    enabled = true
  }

  attribute {
    name = "TestTableHashKey"
    type = "S"
  }

  replica {
    region_name = "eu-east-2"
  }

  replica {
    region_name = "eu-west-2"
  }
}
