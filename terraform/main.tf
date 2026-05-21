terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  app_name = "streamlit-app"
  labels = {
    app         = local.app_name
    environment = var.environment
    managed_by  = "terraform"
  }
}

# Enable required GCP APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "vpcaccess.googleapis.com",
    "servicenetworking.googleapis.com",
    "storage.googleapis.com",
  ])
  service            = each.value
  disable_on_destroy = false
}

# Service account for Cloud Run
resource "google_service_account" "app" {
  account_id   = "${local.app_name}-sa"
  display_name = "Streamlit App Service Account"
}
