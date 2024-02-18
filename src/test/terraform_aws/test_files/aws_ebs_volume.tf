resource "aws_ebs_volume" "without_encryption" {
  availability_zone = "us-west-2a"
  size              = 40

  tags = {
    Name = "HelloWorld"
  }
}

resource "aws_ebs_volume" "encryption_false" {
  availability_zone = "us-west-1a"
  size              = 40
  encrypted         = false

  tags = {
    Name = "HelloWorld"
  }
}

resource "aws_ebs_volume" "i_am_ok" {
  availability_zone = "us-west-2c"
  size              = 40
  encrypted         = true

  tags = {
    Name = "I am ok"
  }
}
