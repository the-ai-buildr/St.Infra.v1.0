locals {
  image = "${var.region}-docker.pkg.dev/${var.project_id}/streamlit-app/app:${var.image_tag}"

  db_connection_name = google_sql_database_instance.app.connection_name
  db_url_sync        = "postgresql+psycopg2://appuser:$(DB_PASSWORD)@/streamlit_app?host=/cloudsql/${local.db_connection_name}"
  db_url_async       = "postgresql+asyncpg://appuser:$(DB_PASSWORD)@/streamlit_app?host=/cloudsql/${local.db_connection_name}"
}

resource "google_cloud_run_v2_service" "app" {
  name     = local.app_name
  location = var.region
  labels   = local.labels

  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.app.email

    scaling {
      min_instance_count = var.cloud_run_min_instances
      max_instance_count = var.cloud_run_max_instances
    }

    vpc_access {
      connector = google_vpc_access_connector.app.id
      egress    = "PRIVATE_RANGES_ONLY"
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.app.connection_name]
      }
    }

    containers {
      image = local.image

      ports {
        container_port = 8501
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }

      env {
        name  = "APP_ENV"
        value = var.environment
      }
      env {
        name  = "GCS_BUCKET_NAME"
        value = google_storage_bucket.uploads.name
      }
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "CLOUD_SQL_CONNECTION_NAME"
        value = google_sql_database_instance.app.connection_name
      }
      env {
        name = "AUTH_COOKIE_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.app["auth_cookie_key"].secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.app["db_password"].secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "DATABASE_URL"
        value = local.db_url_sync
      }
      env {
        name  = "ASYNC_DATABASE_URL"
        value = local.db_url_async
      }
    }
  }

  depends_on = [
    google_project_service.apis,
    google_artifact_registry_repository.app,
    google_sql_database_instance.app,
  ]
}

# Allow unauthenticated public access — remove for IAP-protected apps
resource "google_cloud_run_v2_service_iam_member" "public" {
  name     = google_cloud_run_v2_service.app.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}
