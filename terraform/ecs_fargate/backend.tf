terraform {
  backend "s3" {
    bucket         = "answerking-python-terraform"
    key            = "answerking-python-terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "answerking-python-terraform"
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