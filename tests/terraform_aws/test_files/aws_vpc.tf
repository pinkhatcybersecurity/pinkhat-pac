resource "aws_vpc" "flowlogs_enabled" {
  cidr_block = "127.0.0.1/16"
}

resource "aws_vpc" "missing_flowlogs" {
  cidr_block = "11.0.0.1/16"
}

resource "aws_flow_log" "flowlog_exist" {
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.flowlogs_enabled.id
}
