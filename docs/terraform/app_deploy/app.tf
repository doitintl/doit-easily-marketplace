#the doit-easily cloud run service
resource "google_cloud_run_service" "doit_easily_cloudrun_service" {
  location = var.cloudrun_location
  name     = "doit-easily"
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
          value = var.event_topic
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
      }
    }
  }
}
