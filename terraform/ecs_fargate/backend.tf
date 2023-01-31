terraform {
  backend "s3" {
    bucket         = "answerking-terraform"
    key            = "answerking-terraform-python.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "answerking-terraform-python"
  }
}