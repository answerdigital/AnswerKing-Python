
resource "aws_route53_record" "python" {
  zone_id = var.dns_hosted_zone_id
  name    = var.dns_record_name
  type    = "A"
  ttl     = 300
  set_identifier = "public_ip"
  records = [aws_eip.lb.public_ip]

  geolocation_routing_policy {
    country = "GB"
  }
}

