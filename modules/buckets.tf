resource "aws_s3_bucket" "sagemaker_input_bucket" {
  bucket = "valorantcv-sagemaker-input-bucket"

  tags = {
    Name        = "valorantcv-sagemaker-input-bucket"
    Environment = "dev"
  }
}

resource "aws_s3_bucket" "sagemaker_output_bucket" {
  bucket = "valorant-cv-sagemaker-output-bucket"

  tags = {
    Name        = "valorantcv-sagemaker-output-bucket"
    Environment = "dev"
  }
}

resource "aws_s3_bucket" "yolov4_sagemaker_artifact_bucket" {
  bucket = "valorantcv-yolov4-sagemaker-artifact-bucket"

  tags = {
      Name        = "valorantcv-yolov4-sagemaker-artifact-bucket"
      Environment = "dev"
  }
}

resource "aws_s3_bucket_object" "sagemaker_input_files" {
  bucket = aws_s3_bucket.sagemaker_input_bucket.id

  key = "profile"

  acl = "private"

  source = "../media/selected_frames.zip"

  etag = md5("valorantcv_sagemaker_input_files")
}

# TODO: disable ACL - use policy-based control - https://github.com/hashicorp/terraform-provider-aws/issues/22069