resource "google_storage_bucket" "uploads" {
  name                        = "${var.project_id}-${var.environment}-uploads"
  location                    = var.region
  uniform_bucket_level_access = true
  labels                      = local.labels

  lifecycle_rule {
    condition {
      age = 1
      with_state = "ANY"
      # Clean up incomplete multipart uploads after 1 day
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }

  cors {
    origin          = ["https://*.run.app"]
    method          = ["GET", "PUT", "POST"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }

  depends_on = [google_project_service.apis]
}

resource "google_storage_bucket_iam_member" "app_uploads" {
  bucket = google_storage_bucket.uploads.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.app.email}"
}
