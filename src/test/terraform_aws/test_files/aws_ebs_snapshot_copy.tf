resource "aws_ebs_volume" "simple_volume" {
  availability_zone = "eu-west-1"
  size              = 100

  tags = {
    Name = "Simple Volume"
  }
}

resource "aws_ebs_snapshot" "simple_snapshot" {
  volume_id = aws_ebs_volume.simple_volume.id

  tags = {
    Name = "Taking a snapshot"
  }
}

resource "aws_ebs_snapshot_copy" "vulnerable" {
  source_snapshot_id = aws_ebs_snapshot.simple_snapshot.id
  source_region      = "eu-west-1"

  tags = {
    Name = "Snapshot copy"
  }
}

resource "aws_ebs_snapshot_copy" "good" {
  source_snapshot_id = aws_ebs_snapshot.simple_snapshot.id
  source_region      = "eu-west-1"
  encrypted          = true

  tags = {
    Name = "Snapshot copy good"
  }
}

resource "aws_ebs_snapshot_copy" "vulnerable_false" {
  source_snapshot_id = aws_ebs_snapshot.simple_snapshot.id
  source_region      = "eu-west-1"
  encrypted          = false

  tags = {
    Name = "Snapshot copy vulnerable"
  }
}
