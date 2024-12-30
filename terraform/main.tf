provider "google" {
  credentials = file("<path-to-service-account-key>")
  project     = var.project_id
  region      = var.region
}

module "service_account" {
  source        = "./modules/service_account"
  account_id    = gke-empty-nodes-svc-account
  display_name  = "Cloud Function Service Account"
  project_id    = var.project_id
  role          = "roles/cloudfunctions.invoker"
}

module "my_function" {
  source             = "./modules/cloud_function"
  bucket_name        = var.bucket_name
  source_path        = "../google-cloud-functions/gke-empty-nodes/function.zip"
  function_name      = "gke-empty-nodes"
  description        = "This function checks for empty GKE nodes"
  runtime            = "python39"
  entry_point        = "list_pods"
  region             = var.region
  memory_mb          = 256
  timeout            = 240
  trigger_http       = true
  service_account_email = module.service_account.service_account_email
  environment_variables = {
    LOG_LEVEL = "INFO"
    PROJECT_ID = var.project_id
    ZONE       = var.zone
    CLUSTER_ID = var.cluster_id
  }
  vpc_connector = var.vpc_connector
}