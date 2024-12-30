resource "google_storage_bucket" "function_bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "google_storage_bucket_object" "function_code" {
  name   = "${var.function_name}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = var.source_path
}

resource "google_cloudfunctions_function" "function" {
  name        = var.function_name
  description = var.description
  runtime     = var.runtime
  entry_point = var.entry_point
  region      = var.region

  available_memory_mb   = var.memory_mb
  timeout               = var.timeout
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_code.name

  trigger_http = var.trigger_http
  environment_variables = var.environment_variables
}

