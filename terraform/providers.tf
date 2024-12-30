terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 4.34.0"
    }
    google-beta = {
      source = "hashicorp/google-beta"
      version = "~> 4.34.0"
    }
  }

  required_version = ">= 0.12"
  backend "gcs" {
    bucket  = "bucket-name"
    prefix  = "gke-empty-nodes/state"
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
}

