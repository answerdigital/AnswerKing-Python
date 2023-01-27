# Security groups

resource "aws_security_group" "ecs_sg" {
  vpc_id = module.vpc_subnet_setup.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds_sg" {
  vpc_id = module.vpc_subnet_setup.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = 3306
    to_port         = 3306
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.ecs_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

 # Elastic Container Registry

resource "aws_ecr_repository" "worker" {
  name = "${var.project_name}-repo"
}

# Elastic Container Service

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project_name}-ecs-cluster"

  tags = {
    Name  = "${var.project_name}-ecs"
    Owner = var.owner
  }
}

resource "aws_ecs_service" "service" {
  depends_on = [aws_ecr_repository.worker, module.rds_serverless_cluster_setup.rds_cluster_instance_endpoint, aws_iam_role.ecs_task_execution_role]
  name            = "${var.project_name}-ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type                        = var.service_launch_type
  scheduling_strategy                = var.scheduling_strategy

  network_configuration {
   security_groups  = [aws_security_group.ecs_sg.id]
   subnets          = [module.vpc_subnet_setup.public_subnet_ids[0]]	
   assign_public_ip = true
 }
}

resource "aws_ecs_task_definition" "task_definition" {
  family                = "service"
  network_mode             = var.network_mode
  requires_compatibilities = [var.service_launch_type]
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-container"
      image     = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${aws_ecr_repository.worker.name}:latest"
      cpu       = 2
      essential = true
      networkMode = var.network_mode
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          "awslogs-group": "${var.project_name}-log-group",
          "awslogs-region": var.aws_region,
          "awslogs-stream-prefix": "${var.project_name}-log-stream"
        }
      }
      environment = [
        {"name": "DATABASE_NAME", "value": var.database_name},
        {"name": "DATABASE_HOST", "value": module.rds_serverless_cluster_setup.rds_cluster_instance_endpoint},
        {"name": "DATABASE_PORT", "value": var.database_port},
        {"name": "DATABASE_USER", "value": module.rds_serverless_cluster_setup.rds_cluster_master_username},
        {"name": "DATABASE_PASS", "value": module.rds_serverless_cluster_setup.rds_cluster_master_password},
        {"name": "SECRET_KEY", "value": var.django_secret_key},
        {"name": "DJANGO_SETTINGS_MODULE", "value": var.django_settings_module},
        {"name": "DATABASE_ENGINE", "value": var.django_database_engine}
    
      ]
    }
  ])
}

# IAM policy roles

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole-python"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy-attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Logging

resource "aws_cloudwatch_log_group" "log-group" {
  name              = "${var.project_name}-log-group"
  retention_in_days = 1
}

resource "aws_cloudwatch_log_stream" "log-stream" {
  name           = "${var.project_name}-log-stream"
  log_group_name = aws_cloudwatch_log_group.log-group.name
}