terraform {
  backend "s3" {
    bucket         = "answerking-python-terraform"
    key            = "answerking-python-terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "ak-python-terraform-state"
  }
}

/*

# The commented out code was used to create the s3 bucket and dynamo table.
# It has been removed from the state so will not be impacted by terraform destroy.

resource "aws_s3_bucket" "terraform_backend_bucket" {
  bucket = "answerking-python-terraform"
  tags = {
    Name  = "${var.project_name}-terraform-bucket"
    Owner = var.owner
  }
}

resource "aws_s3_bucket_acl" "terraform_backend_bucket_acl" {
  bucket = aws_s3_bucket.terraform_backend_bucket.id
  acl    = "private"

}

resource "aws_s3_bucket_public_access_block" "terraform_backend_bucket_public_access_block" {
  bucket = aws_s3_bucket.terraform_backend_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "terraform_backend_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_backend_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}
resource "aws_dynamodb_table" "terraform_backend_state" {
 name           = "${var.project_name}-terraform-state"
 read_capacity  = 20
 write_capacity = 20
 hash_key       = "LockID"

 attribute {
   name = "LockID"
   type = "S"
 }

 tags = {
    Name  = "${var.project_name}-dynamo-table"
    Owner = var.owner
  }
}
*/

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

# resource "aws_s3_bucket_policy" "elb_logs_policy" {
#   bucket = aws_s3_bucket.elb_logs.id

#   policy = <<POLICY
#   {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "AWS": "arn:aws:iam::652711504416:root"
#       },
#       "Action": "s3:PutObject",
#       "Resource": "arn:aws:s3:::ak-python-lb-logs/test/AWSLogs/409973623162/*"
#     }
#   ]
# }
# POLICY
# }
#   policy = <<POLICY
#   {
#     "Version": "2012-10-17",
#     "Id": "AWSLogDeliveryWrite",
#     "Statement": [
#         {
#             "Sid": "AWSLogDeliveryAclCheck",
#             "Effect": "Allow",
#             "Principal": {
#                 "Service": "delivery.logs.amazonaws.com"
#                 },
#             "Action": "s3:GetBucketAcl",
#             "Resource": "arn:aws:s3:::ak-python-lb-logs",
#             "Condition": {
#                 "StringEquals": {
#                 "aws:SourceAccount": ["409973623162"]
#                 },
#                 "ArnLike": {
#                 "aws:SourceArn": ["arn:aws:elasticloadbalancing:eu-west-2:409973623162:*"]
#                 }
#             }
#         },
#         {
#             "Sid": "AWSLogDeliveryWrite",
#             "Effect": "Allow",
#             "Principal": {
#                 "Service": "delivery.logs.amazonaws.com"
#             },
#             "Action": "s3:PutObject",
#             "Resource": "arn:aws:s3:::ak-python-lb-logs/AWSLogs/account-ID/*",
#             "Condition": {
#                 "StringEquals": {
#                     "s3:x-amz-acl": "bucket-owner-full-control",
#                     "aws:SourceAccount": ["409973623162"]
#                 },
#                 "ArnLike": {
#                     "aws:SourceArn": ["arn:aws:elasticloadbalancing:eu-west-2:409973623162:*"]
#                 }
#             }
#         }
#     ]
# }
# POLICY
# }

# data "aws_elb_service_account" "main" {}


# data "aws_iam_policy_document" "s3_lb_write" {
#   statement {
#     principals {
#       identifiers = ["${data.aws_elb_service_account.main.arn}"]
#       type = "AWS"
#     }

#     actions = ["s3:PutObject"]

#     resources = [
#       "${aws_s3_bucket.elb_logs.arn}/*"
#     ]
#   }
# }

# resource "aws_s3_bucket_policy" "load_balancer_access_logs_bucket_policy" {
#   bucket = aws_s3_bucket.elb_logs.id
#   policy = data.aws_iam_policy_document.s3_lb_write.json
# }

resource "aws_s3_bucket_acl" "elb_logs_bucket_acl" {
  bucket = aws_s3_bucket.elb_logs.id
  acl    = "private"

}

# resource "aws_s3_bucket_versioning" "terraform_backend_bucket_versioning" {
#   bucket = aws_s3_bucket.elb_logs.id
#   versioning_configuration {
#     status = "Enabled"
#   }
# }



resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.elb_logs.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
    bucket_key_enabled = true
  }
}

#   {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Principal": {
#                 "Service": "logdelivery.elb.amazonaws.com"
#             },
#             "Action": "s3:PutObject",
#             "Resource": "arn:aws:s3:::ak-python-lb-logs/test-lb/AWSLogs/409973623162/*",
#             "Condition": {
#                 "StringEquals": {
#                     "s3:x-amz-acl": "bucket-owner-full-control"
#                 }
#             }
#         }
#     ]
# }