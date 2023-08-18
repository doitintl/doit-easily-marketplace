resource "google_project_service" "compute_engine" {
    project = var.project_id
    service = "compute.googleapis.com"
}

resource "google_project_service" "run" {
    project = var.project_id
    service = "run.googleapis.com"
}

resource "google_project_service" "iap" {
    project = var.project_id
    service = "iap.googleapis.com"
}
resource "google_project_service" "secretmanager" {
    project = var.project_id
    service = "secretmanager.googleapis.com"
}
resource "google_project_service" "cloudcommerceconsumerprocurement" {
    project = var.project_id
    service = "cloudcommerceconsumerprocurement.googleapis.com"
}

resource "google_project_service" "dns" {
    project = var.project_id
    service = "dns.googleapis.com"
}
