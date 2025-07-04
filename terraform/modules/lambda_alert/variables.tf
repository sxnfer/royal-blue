variable "lambda_name" {
  description = "The name of the Lambda function to monitor"
  type        = string
}

variable "filter_pattern" {
  description = "The log pattern to filter"
  type        = string
  default     = "CRITICAL"
}

variable "metric_namespace" {
  description = "CloudWatch metric namespace"
  type        = string
  default     = "Lambda/Custom"
}

variable "alert_emails" {
  description = "List of email addresses to receive SNS notifications"
  type        = list(string)
  default     = []
}
