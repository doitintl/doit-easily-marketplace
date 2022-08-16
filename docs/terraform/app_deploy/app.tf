#the doit-easily cloud run service
resource "google_cloud_run_service" "doit_easily_cloudrun_service" {
  location = var.cloudrun_location
  name     = "doit-easily${local.codelab_suffix}"
  project = local.project_id
  template {
    spec {
      containers {
        image = "gcr.io/doit-public/doit-easily:${var.doit_easily_version}"
        env {
          name  = "SLACK_WEBHOOK"
          value = var.slack_webhook
        }
        env {
          name  = "EVENT_TOPIC"
          value = var.event_topic_name != "" ? google_pubsub_topic.event_topic.id : ""
        }
        env {
          name  = "IS_CODELAB"
          value = var.is_codelab
        }
        env {
          name  = "MARKETPLACE_PROJECT"
          value = var.marketplace_project
        }
        env {
          name  = "BACKEND_PROJECT"
          value = var.backend_project
        }
        env {
          name  = "SUBSCRIPTION_ID"
          value = var.subscription_id
        }
        env {
          name  = "AUTO_APPROVE_ENTITLEMENTS"
          value = var.auto_approve_entitlements
        }
        env {
          name  = "ENABLE_PUSH_ENDPOINT"
          value = var.enable_push_endpoint
        }
        env {
          name  = "LOG_LEVEL"
          value = var.log_level
        }
        env {
          name  = "AUDIENCE"
          value = var.audience
        }
      }
      service_account_name = data.google_service_account.doit_easily_backend_integration_sa.email
    }
#    metadata {
#      annotations = {
#        # For valid annotation values and descriptions, see
#        # https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress
#        "run.googleapis.com/ingress" = "internal"
#      }
#    }
  }
}
#for now, until IAP or API gateway is setup
resource "google_cloud_run_service_iam_member" "davec_invoker" {
  member  = "user:dave.c@doit-intl.com"
  role    = "roles/run.invoker"
  service = google_cloud_run_service.doit_easily_cloudrun_service.name
  location = var.cloudrun_location
  project = local.project_id
}

#for now, until IAP or API gateway is setup
resource "google_cloud_run_service_iam_member" "alfredo_invoker" {
  member  = "user:alfredo@doit-intl.com"
  role    = "roles/run.invoker"
  service = google_cloud_run_service.doit_easily_cloudrun_service.name
  location = var.cloudrun_location
  project = local.project_id
}


##allow allUsers to invoke, service is secured with IAP!
#resource "google_cloud_run_service_iam_member" "allUsers_invoker" {
#  member  = "allUsers"
#  role    = "roles/run.invoker"
#  service = google_cloud_run_service.doit_easily_cloudrun_service.id
#}

#we need to do this for IAP in cloudrun https://cloud.google.com/iap/docs/identity-howto per https://cloud.google.com/iap/docs/enabling-cloud-run#before_you_begin