resource "aws_s3_bucket" "elb_logs" {
  bucket = "${var.project_name}-lb-logs"
  acl    = "private"

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

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.elb_logs.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
    bucket_key_enabled = true
  }
}