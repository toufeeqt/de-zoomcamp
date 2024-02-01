terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.14.0"
    }
  }
}

provider "google" {
  credentials = file(var.gcp_credentials)
  project     = var.gcp_project_id
  region      = var.gcp_region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  storage_class = var.gcs_storage_class
  location      = var.gcp_location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id                  = var.bq_dataset_name
  location                    = var.gcp_location

}