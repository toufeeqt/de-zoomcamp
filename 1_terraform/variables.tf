variable "gcp_credentials" {
    description = "GCP credentials"
    default = "./keys/gcp.json"
  
}
variable "gcp_project_id" {
    description = "GCP Project ID"
    default = "de-zoomcamp-413005"
}

variable "gcp_region" {
    description = "GCP Region location"
    default = "europe-west4"
}

variable "gcp_location" {
    description = "GCP location"
    default = "EU"
}

variable "bq_dataset_name" {
    description = "GBQ dataset name"
    default = "demo_dataset"
}

variable "gcs_bucket_name" {
    description = "GCS bucket name"
    default = "de-zoomcamp-413005-demo-bucket"
}
variable "gcs_storage_class" {
    description = "GCS storage class"
    default = "STANDARD"
}