resource "aws_cloudwatch_log_group" "log-group" {
  name              = "${var.project_name}-log-group"
  retention_in_days = 1
}

resource "aws_cloudwatch_log_stream" "log-stream" {
  name           = "${var.project_name}-log-stream"
  log_group_name = aws_cloudwatch_log_group.log-group.name
}