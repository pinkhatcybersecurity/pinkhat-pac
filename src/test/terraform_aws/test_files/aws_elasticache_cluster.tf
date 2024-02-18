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
  num_cache_nodes   = 1
  port              = 6379
  apply_immediately = true
}
