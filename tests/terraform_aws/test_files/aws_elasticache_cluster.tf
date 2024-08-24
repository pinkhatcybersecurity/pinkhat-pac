resource "aws_elasticache_cluster" "transit_enabled" {
  cluster_id        = "encryption_in_transit"
  engine            = "redis"
  node_type         = "cache.t3.micro"
  num_cache_nodes   = 1
  port              = 6379
  apply_immediately = true
  transit_encryption_enabled = true
}

resource "aws_elasticache_cluster" "no_encryption_in_transit" {
  cluster_id        = "no_encryption_in_transit"
  engine            = "redis"
  node_type         = "cache.t3.micro"
  maintenance_window = "sun:5:00-sun:9:00"
  num_cache_nodes   = 1
  port              = 6379
  apply_immediately = true
}

resource "aws_elasticache_cluster" "contains_both_log_delivery_configuration" {
  cluster_id        = "ahoj"
  engine            = "redis"
  node_type         = "cache.t3.micro"
  num_cache_nodes   = 1
  port              = 6379
  apply_immediately = true
  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.tada.name
    destination_type = "cloudwatch-logs"
    log_format       = "text"
    log_type         = "slow-log"
  }
  log_delivery_configuration {
    destination      = aws_kinesis_firehose_delivery_stream.tada.name
    destination_type = "kinesis-firehose"
    log_format       = "json"
    log_type         = "engine-log"
  }
}

resource "aws_elasticache_cluster" "onlyfirehose" {
  cluster_id        = "firehose_check"
  engine            = "redis"
  node_type         = "cache.t3.micro"
  num_cache_nodes   = 1
  port              = 6379
  apply_immediately = true
  log_delivery_configuration {
    destination      = aws_kinesis_firehose_delivery_stream.example.name
    destination_type = "kinesis-firehose"
    log_format       = "text"
    log_type         = "engine-log"
  }
}
