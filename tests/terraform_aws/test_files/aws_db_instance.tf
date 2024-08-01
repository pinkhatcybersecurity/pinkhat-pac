data "aws_kms_key" "kms_key_id" {
  key_id = "niceone-ef98987289372"
}

data "aws_rds_orderable_db_instance" "hello_rds" {
  engine                     = "hello_rds-ee" # CEV engine to be used
  engine_version             = "something"      # CEV engine version to be used
  license_model              = "bring-your-own-license"
  storage_type               = "gp3"
  preferred_instance_classes = ["db.r5.xlarge", "db.r5.2xlarge", "db.r5.4xlarge"]
}

resource "aws_db_instance" "vulnerable_default" {
  allocated_storage           = 100
  auto_minor_version_upgrade  = false
  custom_iam_instance_profile = "AWSRDSCustomInstanceProfile"
  publicly_accessible         = true
  backup_retention_period     = 5
  db_subnet_group_name        = local.db_subnet_group_name
  engine                      = data.aws_rds_orderable_db_instance.hello_rds.engine
  engine_version              = data.aws_rds_orderable_db_instance.hello_rds.engine_version
  identifier                  = "ee-should-be-vulnerable"
  instance_class              = data.aws_rds_orderable_db_instance.hello_rds.instance_class
  kms_key_id                  = data.aws_kms_key.kms_key_id.arn
  license_model               = data.aws_rds_orderable_db_instance.hello_rds.license_model
  multi_az                    = false
  password                    = "I'm happy plain text password"
  username                    = "test"
  storage_encrypted           = false
  enabled_cloudwatch_logs_exports = ["audit", "error", "general"]

  timeouts {
    create = "3h"
    delete = "3h"
    update = "3h"
  }
}

resource "aws_db_instance" "test-replica" {
  replicate_source_db         = aws_db_instance.vulnerable_default.identifier
  replica_mode                = "mounted"
  maintenance_window          = "Mon:00:00-Mon:03:00"
  auto_minor_version_upgrade  = false
  custom_iam_instance_profile = "AWSRDSCustomInstanceProfile" # Instance profile is required for Custom for Oracle. See: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-setup-orcl.html#custom-setup-orcl.iam-vpc
  backup_retention_period     = 7
  identifier                  = "ee-instance-replica"
  instance_class              = data.aws_rds_orderable_db_instance.hello_rds.instance_class
  kms_key_id                  = data.aws_kms_key.kms_key_id.arn
  multi_az                    = false
  skip_final_snapshot         = true
  storage_encrypted           = true
}


output "password_in_state_file" {
  value = aws_db_instance.vulnerable_default.password
}

# Generate a random password (optional but recommended)
resource "random_password" "master" {
  length           = 16
  special          = true
  override_special = "_!%^"
}

# Create a secret in AWS Secrets Manager
resource "aws_secretsmanager_secret" "password" {
  name = "test-db-password"
}

# Associate the secret value with the random password
resource "aws_secretsmanager_secret_version" "password" {
  secret_id     = aws_secretsmanager_secret.password.id
  secret_string = random_password.master.result
}

# Use the secret in your RDS instance configuration
resource "aws_db_instance" "secret_manager" {
  identifier        = "testdb"
  allocated_storage = 20
  storage_type      = "gp2"
  engine            = "aurora-postgresql"
  engine_version    = "5.7"
  instance_class    = "db.t2.medium"
  username          = "dbadmin"
  password          = aws_secretsmanager_secret_version.password.secret_string
  enabled_cloudwatch_logs_exports = ["update", "postgresql"]
}
