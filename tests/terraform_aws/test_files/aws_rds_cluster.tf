resource "aws_rds_cluster" "no_cloud_watch" {
  cluster_identifier = "example"
  engine             = "aurora-postgresql"
  engine_mode        = "provisioned"
  engine_version     = "13.6"
  database_name      = "test"
  master_username    = "test"
  master_password    = "must_be_eight_characters"
  storage_encrypted  = true
  deletion_protection = true
  preferred_maintenance_window = "Mon:00:00-Mon:03:00"

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster_instance" "example" {
  cluster_identifier = aws_rds_cluster.no_cloud_watch.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.no_cloud_watch.engine
  engine_version     = aws_rds_cluster.no_cloud_watch.engine_version
}

resource "aws_rds_cluster" "nothing" {
  cluster_identifier = "example"
  engine             = "aurora-postgresql"
  engine_mode        = "provisioned"
  engine_version     = "13.6"
  database_name      = "test"
  master_username    = "test"
  master_password    = "must_be_eight_characters"
  preferred_maintenance_window = "Tue:00:00-Tue:03:00"

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster" "cloud_watch_enabled" {
  cluster_identifier = "example"
  engine             = "aurora-postgresql"
  engine_mode        = "provisioned"
  engine_version     = "13.6"
  database_name      = "test"
  master_username    = "test"
  master_password    = "must_be_eight_characters"
  enabled_cloudwatch_logs_exports = ["audit"]
  backup_retention_period = 7
  preferred_maintenance_window = "Sun:00:00-Sun:03:00"

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster" "cloud_watch_enabled_all" {
  cluster_identifier = "example"
  engine             = "aurora-postgresql"
  engine_mode        = "provisioned"
  engine_version     = "13.6"
  database_name      = "test"
  master_username    = "test"
  master_password    = "must_be_eight_characters"
  enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery", "postgresql"]
  backup_retention_period = 9

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster" "cloud_watch_enabled_mssql_all" {
  cluster_identifier = "example"
  engine             = "aurora-mssql"
  engine_mode        = "provisioned"
  engine_version     = "13.6"
  database_name      = "test"
  master_username    = "test"
  master_password    = "must_be_eight_characters"
  enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery"]
  backup_retention_period = 8

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}
