resource "aws_route53_record" "python" {
  zone_id = var.dns_hosted_zone_id
  name    = var.dns_record_name
  type    = "A"
  ttl     = 300
  records = [aws_eip.lb.public_ip]
}