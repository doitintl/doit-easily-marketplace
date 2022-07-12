#the SA that the doit-easily cloud run service runs as (created during project creation)
data "google_service_account" "doit_easily_backend_integration_sa" {
  account_id = "doit-easily"
  project = var.marketplace_project
}

#allow doit-easily to edit pubsub on this project
resource "google_project_iam_member" "doit_easily_pubsub_editor" {
  member  = "serviceAccount:${data.google_service_account.doit_easily_backend_integration_sa.email}"
  # because the subscription must be created in the marketplace project
  project = var.marketplace_project
  role    = "roles/pubsub.editor"
}

#allow the doit-easily SA to invoke the cloudrun app
resource "google_cloud_run_service_iam_member" "doit_easily_cloudrun_invoker" {
  member  = "serviceAccount:${data.google_service_account.doit_easily_backend_integration_sa.email}"
  project = local.project_id
  role    = "roles/run.invoker"
  service = google_cloud_run_service.doit_easily_cloudrun_service.name
  location = var.cloudrun_location
}