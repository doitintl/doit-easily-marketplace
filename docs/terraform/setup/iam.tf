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
  project = var.project_id
}

#allow doit-easily to create tokens as itself (required for push pubsub subscription authentication)
resource "google_service_account_iam_member" "doit_easily_token_creator" {
  member             = "serviceAccount:${google_service_account.doit_easily_backend_integration_sa.email}"
  role               = "roles/iam.serviceAccountTokenCreator"
  service_account_id = google_service_account.doit_easily_backend_integration_sa.id
}

#allow doit-easily to use itself (required for push pubsub subscription authentication)
resource "google_service_account_iam_member" "doit_easily_sa_user" {
  member             = "serviceAccount:${google_service_account.doit_easily_backend_integration_sa.email}"
  role               = "roles/iam.serviceAccountUser"
  service_account_id = google_service_account.doit_easily_backend_integration_sa.id
}

#the SA used for the saas-codelab
resource "google_service_account" "saas_codelab_backend_integration_sa" {
  account_id = "saas-codelab"
  description = "Saas codelab backend integration"
  project = var.project_id
}

#allowsaas-codelab to create tokens as itself (required for push pubsub subscription authentication)
resource "google_service_account_iam_member" "saas_codelab_token_creator" {
  member             = "serviceAccount:${google_service_account.saas_codelab_backend_integration_sa.email}"
  role               = "roles/iam.serviceAccountTokenCreator"
  service_account_id = google_service_account.saas_codelab_backend_integration_sa.id
}

#allow saas-codelab to use itself (required for push pubsub subscription authentication)
resource "google_service_account_iam_member" "saas_codelab_sa_user" {
  member             = "serviceAccount:${google_service_account.saas_codelab_backend_integration_sa.email}"
  role               = "roles/iam.serviceAccountUser"
  service_account_id = google_service_account.saas_codelab_backend_integration_sa.id
}