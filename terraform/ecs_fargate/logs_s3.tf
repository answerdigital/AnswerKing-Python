resource "aws_s3_bucket" "elb_logs" {
  bucket = "${var.project_name}-lb-logs"

  tags = {
    Name  = "${var.project_name}-lb-logs"
    Owner = var.owner
  }
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_elb_service_account" "main" {}
resource "aws_s3_bucket_policy" "lb-bucket-policy" {
  bucket = aws_s3_bucket.elb_logs.id

  policy = <<POLICY
{
    "Id": "Policy",
    "Version": "2012-10-17",
    "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "${data.aws_elb_service_account.main.arn}"
                ]
            },
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "${aws_s3_bucket.elb_logs.arn}/AWSLogs/*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "delivery.logs.amazonaws.com"
            },
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "${aws_s3_bucket.elb_logs.arn}/AWSLogs/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "delivery.logs.amazonaws.com"
            },
            "Action": [
                "s3:GetBucketAcl"
            ],
            "Resource": "${aws_s3_bucket.elb_logs.arn}"
        }
    ]
}
POLICY
}

resource "aws_s3_bucket_acl" "elb_logs_bucket_acl" {
  bucket = aws_s3_bucket.elb_logs.id
  acl    = "private"

}

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.elb_logs.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "elb_logs_backend_bucket_public_access_block" {
  bucket                  = aws_s3_bucket.elb_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}