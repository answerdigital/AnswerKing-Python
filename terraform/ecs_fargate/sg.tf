resource "aws_security_group" "ecs_sg" {
  vpc_id = module.vpc_subnet_setup.vpc_id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name  = "${var.project_name}-ecs-sg"
    Owner = var.owner
  }
}

resource "aws_security_group" "rds_sg" {
  vpc_id = module.vpc_subnet_setup.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = var.database_port
    to_port         = var.database_port
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.ecs_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name  = "${var.project_name}-rds-sg"
    Owner = var.owner
  }
}

resource "aws_security_group" "lb_sg" {
  #checkov:skip=CKV_AWS_260:Allowing ingress from 0.0.0.0 for public HTTP(S) access
  name        = "${var.project_name}-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id       = module.vpc_subnet_setup.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All traffic"
  }

  tags = {
    Name  = "${var.project_name}-alb-sg"
    Owner = var.owner
  }
}
