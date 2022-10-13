# the topic doit-easily publishes to (optional)
resource "google_pubsub_topic" "event_topic" {
  count = var.event_topic_name != "" ? 1 : 0
  name = "${var.event_topic_name}${local.codelab_suffix}"
  project = local.project_id
}

resource "google_pubsub_topic_iam_member" "event_topic_doit_easily_publisher" {
  count = var.event_topic_name != "" ? 1 : 0
  member = "serviceAccount:${data.google_service_account.doit_easily_backend_integration_sa.email}"
  role   = "roles/pubsub.publisher"
  topic  = google_pubsub_topic.event_topic[0].name
}

#the subscription that get entitlement messages from Google
resource "google_pubsub_subscription" "doit_easily_subscription" {
  name     = "doit-easily${local.codelab_suffix}"
  topic    = local.topic
  provider = google.prod_impersonation # get created as doit-easily SA, not the user running this terraform
  #  this must be deployed into the marketplace project
  project  = var.marketplace_project
  push_config {
    push_endpoint = "${google_cloud_run_service.doit_easily_cloudrun_service.status[0].url}/notification"
    oidc_token {
      service_account_email = data.google_service_account.doit_easily_backend_integration_sa.email
    }
  }
}