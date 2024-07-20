resource "aws_ebs_snapshot_import" "ok" {
  disk_container {
    format = "VHD"
    user_bucket {
      s3_bucket = "disk-images"
      s3_key    = "source.vhd"
    }
  }

  role_name = "disk-image-import"

  tags = {
    Name = "HelloWorld"
  }
  encrypted = true
}

resource "aws_ebs_snapshot_import" "vulnerable" {
  disk_container {
    format = "VHD"
    user_bucket {
      s3_bucket = "disk-images"
      s3_key    = "source.vhd"
    }
  }

  role_name = "disk-image-import"

  tags = {
    Name = "HelloWorld"
  }
}

resource "aws_ebs_snapshot_import" "vulnerable_false" {
  disk_container {
    format = "VHD"
    user_bucket {
      s3_bucket = "disk-images"
      s3_key    = "source.vhd"
    }
  }

  role_name = "disk-image-import"

  tags = {
    Name = "HelloWorld"
  }
  encrypted = false
}
