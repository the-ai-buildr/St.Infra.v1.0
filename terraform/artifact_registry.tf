resource "google_artifact_registry_repository" "app" {
  repository_id = "streamlit-app"
  format        = "DOCKER"
  location      = var.region
  description   = "Streamlit app Docker images"
  labels        = local.labels

  depends_on = [google_project_service.apis]
}

# Grant Cloud Run SA permission to pull images
resource "google_artifact_registry_repository_iam_member" "app_reader" {
  repository = google_artifact_registry_repository.app.name
  location   = var.region
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.app.email}"
}
