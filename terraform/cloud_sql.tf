resource "google_sql_database_instance" "app" {
  name             = "${local.app_name}-${var.environment}"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier = var.db_tier
    labels = local.labels

    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.app.id
      enable_private_path_for_google_cloud_services = true
    }

    backup_configuration {
      enabled = var.environment == "production"
    }
  }

  deletion_protection = var.environment == "production"
  depends_on          = [google_service_networking_connection.private_vpc]
}

resource "google_sql_database" "app" {
  name     = "streamlit_app"
  instance = google_sql_database_instance.app.name
}

resource "google_sql_user" "app" {
  name     = "appuser"
  instance = google_sql_database_instance.app.name
  password = var.db_password
}

# Allow Cloud Run SA to connect to Cloud SQL
resource "google_project_iam_member" "sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app.email}"
}
