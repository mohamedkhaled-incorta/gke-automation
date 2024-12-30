variable "account_id" {
  description = "Service account ID"
  type        = string
}

variable "display_name" {
  description = "Display name for the service account"
  type        = string
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "role" {
  description = "IAM role to attach to the service account"
  type        = string
}

