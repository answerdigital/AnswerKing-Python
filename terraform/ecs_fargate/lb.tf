resource "aws_lb" "lb" {
  name               = "${var.project_name}-lb"
  load_balancer_type = var.lb_type
  internal           = false
  subnets            = module.vpc_subnet_setup.private_subnet_ids
  drop_invalid_header_fields = true
  security_groups    = [aws_security_group.lb_sg.id]

  access_logs {
    bucket  = aws_s3_bucket.elb_logs.bucket
    enabled = true
  }

  tags = {
    Name  = "${var.project_name}-lb"
    Owner = var.owner
  }
}

resource "aws_lb_target_group" "target" {
  name        = "${var.project_name}-lb-target-group"
  port        = var.host_port
  protocol    = "HTTPS"
  target_type = "ip"
  vpc_id      = module.vpc_subnet_setup.vpc_id

  health_check {
    healthy_threshold   = "3"
    interval            = "300"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/healthcheck/"
    unhealthy_threshold = "2"
  }
  tags = {
    Name  = "${var.project_name}-lb-target-group"
    Owner = var.owner
  }
}


resource "aws_acm_certificate" "cert" {
  domain_name       = var.dns_record_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_listener" "listener_http_redirect_https" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.lb.arn
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target.id
  }

  tags = {
    Name  = "${var.project_name}-lb-listener"
    Owner = var.owner
  }
}


