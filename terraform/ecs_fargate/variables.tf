variable "aws_region" {
    type = string
    description = "AWS Region to use for resources"
    default = "eu-west-2"
}

variable "project_name" {
  description = "Project name to use in resource names"
  default     = "ak-python"
}

variable "owner" {
  description = "Project owner to use in resource names"
  default     = "answerking-python-team"
}

variable "image_url" {
  type        = string
  description = "AnswerKing Python image"
  default     = "ghcr.io/ananswerconsulting/answerking-python:latest"
}

# Database variables

variable "database_name" {
    type = string
    description = "Database name."
    default = "python_test_database"
}

variable "database_port" {
    type = string
    description = "Database port."
    default = "3306"
}

variable "django_settings_module" {
    type = string
    description = "Django settings module."
    default = "answerking.settings.base"
}

variable "database_engine" {
    type = string
    description = "Database engine."
    default = "aurora-mysql"
}

variable "database_engine_version" {
    type = string
    description = "Database engine."
    default = "8.0.mysql_aurora.3.02.0"
}

variable "django_database_engine" {
    type = string
    description = "Django database engine."
    default = "django.db.backends.mysql"
}

# ECS variables

variable "service_launch_type" {
    type = string
    description = "ECS service laucnh type."
    default = "FARGATE"
}

variable "scheduling_strategy" {
    type = string
    description = "ECS service scheduling strategy."
    default = "REPLICA"
}

variable "container_port" {
    type = number
    description = "Container port."
    default = 8000
}

variable "host_port" {
    type = number
    description = "Container port."
    default = 8000
}

variable "network_mode" {
    type = string
    description = "Network mode."
    default = "awsvpc"
}

variable "ecs_task_cpu" {
    type = number
    description = "Task CPU."
    default = 512
}

variable "ecs_task_memory" {
    type = number
    description = "Task memory."
    default = 1024
}