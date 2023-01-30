resource "aws_ecr_repository" "worker" {
  name = "${var.project_name}-registry"

  tags = {
    Name  = "${var.project_name}-registry"
    Owner = var.owner
  }
}