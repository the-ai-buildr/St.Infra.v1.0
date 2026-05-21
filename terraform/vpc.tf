resource "google_compute_network" "app" {
  name                    = "${local.app_name}-vpc"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.apis]
}

resource "google_compute_subnetwork" "app" {
  name          = "${local.app_name}-subnet"
  ip_cidr_range = "10.10.0.0/24"
  region        = var.region
  network       = google_compute_network.app.id
}

# Serverless VPC connector — lets Cloud Run reach Cloud SQL on private IP
resource "google_vpc_access_connector" "app" {
  name          = "${local.app_name}-connector"
  region        = var.region
  subnet {
    name = google_compute_subnetwork.app.name
  }
  machine_type  = "e2-micro"
  min_instances = 2
  max_instances = 3
  depends_on    = [google_project_service.apis]
}

# Private services access for Cloud SQL
resource "google_compute_global_address" "private_ip_range" {
  name          = "${local.app_name}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.app.id
}

resource "google_service_networking_connection" "private_vpc" {
  network                 = google_compute_network.app.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_range.name]
  depends_on              = [google_project_service.apis]
}
