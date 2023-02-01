provider "aws" {
  region = "eu-west-2"
  skip_credentials_validation = true
}

module "vpc_subnet_setup" {
  source = "git::https://github.com/AnswerConsulting/AnswerKing-Infrastructure.git//Terraform_modules/vpc_subnets?ref=v1.0.0"
  project_name = var.project_name
  owner = var.owner
  num_public_subnets = 1
  num_private_subnets = 2
}

module "rds_serverless_cluster_setup" {
  source = "git::https://github.com/AnswerConsulting/AnswerKing-Infrastructure.git//Terraform_modules/rds_serverless_cluster?ref=v1.0.0"
  project_name = var.project_name
  owner = var.owner
  database_name = var.database_name
  database_engine = var.database_engine
  database_engine_version = var.database_engine_version
  database_subnet_ids = module.vpc_subnet_setup.private_subnet_ids
  database_availability_zone = module.vpc_subnet_setup.az_zones[0]
  database_security_groups = [aws_security_group.rds_sg.id]
}