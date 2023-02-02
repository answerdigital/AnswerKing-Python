resource "aws_eip" "lb" {
  vpc = true

  tags = {
    Name  = "${var.project_name}-eip"
    Owner = var.owner
  }
}

resource "aws_lb" "eip_lb" {
  name               = "${var.project_name}-lb"
  load_balancer_type = "network"
  internal           = false
  ip_address_type    = "ipv4"

  subnet_mapping {
    subnet_id     = "${module.vpc_subnet_setup.public_subnet_ids[0]}"
    allocation_id = "${aws_eip.lb.id}"
  }

  tags = {
    Name  = "${var.project_name}-lb"
    Owner = var.owner
  }
}

resource "aws_lb_target_group" "eip_target" {
  name        = "tf-example-lb-tg"
  port        = 8000
  protocol    = "TCP"
  target_type = "ip"
  vpc_id      = module.vpc_subnet_setup.vpc_id

  tags = {
    Name  = "${var.project_name}-lb-target-group"
    Owner = var.owner
  }
}

resource "aws_lb_listener" "eip_listener" {
  load_balancer_arn = aws_lb.eip_lb.arn
  port              = 8000
  protocol          = "TCP"
  

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.eip_target.arn
  }
}