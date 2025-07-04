resource "aws_lambda_function" "lambda" {
  s3_bucket        = var.s3_bucket.id
  s3_key           = module.dependency_layer.layer_zip_filename
  function_name    = var.function_name
  handler          = "src.lambdas.${var.function_name}.lambda_handler"
  runtime          = var.python_runtime
  source_code_hash = filebase64sha256("${path.root}/../dist/${var.function_name}.zip")
  role             = aws_iam_role.iam_for_lambda.arn
  timeout          = 200
  environment {
    variables = {
      INGEST_ZONE_BUCKET_NAME  = var.ingest_zone_bucket.id
      LAMBDA_STATE_BUCKET_NAME = var.lambda_state_bucket.id
      TOTESYS_DB_USER          = var.TOTESYS_DB_USER
      TOTESYS_DB_PASSWORD      = var.TOTESYS_DB_PASSWORD
      TOTESYS_DB_HOST          = var.TOTESYS_DB_HOST
      TOTESYS_DB_DATABASE      = var.TOTESYS_DB_DATABASE
      TOTESYS_DB_PORT          = var.TOTESYS_DB_PORT
    }
  }

  layers     = [module.dependency_layer.aws_lambda_layer_version.arn, "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python313:1"]
  depends_on = [module.dependency_layer.layer_build_resource, aws_s3_object.lambda_src_object, module.dependency_layer.lambda_layer_object]
}

resource "null_resource" "run_lambda_build_script" {
  provisioner "local-exec" {
    working_dir = "${path.root}/../"
    command     = "./build_${var.function_name}_zip.sh"
  }
  triggers = {
    lock_file_hash = filebase64sha256("${path.root}/../uv.lock")
    src_hash       = sha256(join("", [for f in fileset("${path.root}/../src", "**") : filesha256("${path.root}/../src/${f}")]))
  }
}

resource "aws_s3_object" "lambda_src_object" {
  bucket     = var.s3_bucket.id
  key        = module.dependency_layer.layer_zip_filename
  source     = "${path.root}/../dist/${var.function_name}.zip"
  etag       = filemd5("${path.root}/../dist/${var.function_name}.zip")
  depends_on = [var.s3_bucket]
}

module "dependency_layer" {
  source         = "../lambdas_layer"
  python_runtime = var.python_runtime
  lambda_layers_bucket = {
    arn = var.lambda_layers_bucket.arn
    id  = var.lambda_layers_bucket.id
  }
}
