output "service_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_v2_service.app.uri
}

output "artifact_registry_repo" {
  description = "Artifact Registry Docker repository path"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app.repository_id}"
}

output "cloud_sql_connection_name" {
  description = "Cloud SQL instance connection name (for CLOUD_SQL_CONNECTION_NAME env var)"
  value       = google_sql_database_instance.app.connection_name
}

output "uploads_bucket" {
  description = "GCS uploads bucket name"
  value       = google_storage_bucket.uploads.name
}

output "service_account_email" {
  description = "Cloud Run service account email"
  value       = google_service_account.app.email
}
