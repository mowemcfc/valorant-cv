resource "aws_iam_role" "carter-dev-role" {
  name = "sagemaker-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      },

    ]
  })
}


resource "aws_iam_policy" "sagemaker_s3_rw_policy" {
  name = "sagemaker_s3_rw_policy"
  description = "Allows sagemaker read+write access to all s3"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action" : [
          "s3:*"
        ],
        Effect: "Allow",
        Resource: "*"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "sagemaker_rw_access_attachment" {
  name = "sagemaker_rw_access_attachment"
  roles = [aws_iam_role.carter-dev-role.name]
  policy_arn = aws_iam_policy.sagemaker_s3_rw_policy.arn
}