#give google access to this project
resource "google_project_iam_member" "cloud-commerce-marketplace-onboarding_editor" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-marketplace-onboarding@twosync-src.google.com"
  role    = "roles/editor"
}

#give google access to this project
resource "google_project_iam_member" "cloud-commerce-marketplace_admin" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-marketplace-onboarding@twosync-src.google.com"
  role    = "roles/servicemanagement.admin"
}

#give google access to this project
resource "google_project_iam_member" "cloud-commerce-procurement_serviceConsumer" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-procurement@system.gserviceaccount.com"
  role    = "roles/servicemanagement.serviceConsumer"
}

#give google access to this project
resource "google_project_iam_member" "cloud-commerce-procurement_serviceController" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-procurement@system.gserviceaccount.com"
  role    = "roles/servicemanagement.serviceController"
}


#the SA that the doit-easily cloud run service runs as
resource "google_service_account" "doit_easily_backend_integration_sa" {
  account_id = "doit-easily"
  description = "Doit Easily backend integration"
  project = local.project_id
}