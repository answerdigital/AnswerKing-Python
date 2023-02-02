resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project_name}-ecs-cluster"

  tags = {
    Name  = "${var.project_name}-ecs"
    Owner = var.owner
  }
}

resource "aws_ecs_service" "service" {
  depends_on = [
                module.rds_serverless_cluster_setup.rds_cluster_instance_endpoint,
                aws_iam_role.ecs_task_execution_role
                ]
  name            = "${var.project_name}-ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type                        = var.service_launch_type
  scheduling_strategy                = var.scheduling_strategy
  load_balancer {
    target_group_arn = aws_lb_target_group.eip_target.arn
    container_name   = "${var.project_name}-container"
    container_port   =  8000

  }

  network_configuration {
   security_groups  = [aws_security_group.ecs_sg.id]
   subnets          = [module.vpc_subnet_setup.public_subnet_ids[0]]
   assign_public_ip = true
 }

 tags = {
    Name  = "${var.project_name}-service"
    Owner = var.owner
  }
}

resource "aws_ecs_task_definition" "task_definition" {
  family                   = "${var.project_name}-task"
  network_mode             = var.network_mode
  requires_compatibilities = [var.service_launch_type]
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-container"
      image     = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.project_name}-repo:latest"
      cpu       = 256
      essential = true
      networkMode = var.network_mode
      portMappings = [
        {
          containerPort = "${var.container_port}"
          hostPort      = "${var.host_port}"
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

  tags = {
    Name  = "${var.project_name}-task-definition"
    Owner = var.owner
  }
}
