
resource "aws_route53_record" "python" {
  zone_id = var.dns_hosted_zone_id
  name    = var.dns_record_name
  type    = "CNAME"
  set_identifier = "public_ip"
  ttl = "60"
  records = [aws_lb.lb.dns_name]
  geolocation_routing_policy {
    country = "GB"
  }
}

