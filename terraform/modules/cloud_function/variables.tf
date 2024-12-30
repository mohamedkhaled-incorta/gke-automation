variable "bucket_name" {
  description = "Name of the bucket to store the function code"
  type        = string
}

variable "source_path" {
  description = "Path to the function code archive"
  type        = string
}

variable "function_name" {
  description = "Name of the Cloud Function"
  type        = string
}

variable "description" {
  description = "Description of the Cloud Function"
  type        = string
  default     = ""
}

variable "runtime" {
  description = "Runtime for the Cloud Function (e.g., python39)"
  type        = string
}

variable "entry_point" {
  description = "Entry point of the Cloud Function"
  type        = string
}

variable "region" {
  description = "Region to deploy the Cloud Function"
  type        = string
}

variable "memory_mb" {
  description = "Memory allocated to the Cloud Function"
  type        = number
  default     = 256
}

variable "timeout" {
  description = "Timeout for the Cloud Function in seconds"
  type        = number
  default     = 60
}

variable "trigger_http" {
  description = "Whether the function is triggered by HTTP"
  type        = bool
  default     = true
}

variable "environment_variables" {
  description = "Environment variables for the Cloud Function"
  type        = map(string)
  default     = {}
}

