#the doit-easily cloud run service
resource "google_cloud_run_service" "doit_easily_cloudrun_service" {
  location = var.cloudrun_location
  name     = "doit-easily${local.codelab_suffix}"
  project = var.project_id
  template {
    spec {
      containers {
        image = var.doit_easily_image
        env {
          name  = "SLACK_WEBHOOK"
          value = var.slack_webhook
        }
        env {
          name  = "EVENT_TOPIC"
          value = var.event_topic_name != "" ? google_pubsub_topic.event_topic[0].id : ""
        }
        env {
          name  = "IS_CODELAB"
          value = var.is_codelab
        }
        env {
          name  = "MARKETPLACE_PROJECT"
          value = var.project_id
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
        volume_mounts {
          name       = "toml-config"
          mount_path = "/config/"
        }
      }
      volumes {
        name = "toml-config"
        secret {
          secret_name = "settings-toml"
          #          default_mode = 292 # 0444
          items {
            key  = "1"
            path = "custom-settings.toml" # name of file
            #            mode = 256 # 0400
          }
        }
      }
      service_account_name = local.service_account_email
    }
  }
    metadata {
      annotations = {
        # For valid annotation values and descriptions, see
        # https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress
        "run.googleapis.com/ingress" = "internal-and-cloud-load-balancing"
      }
    }
}



resource "google_cloud_run_service_iam_binding" "doit_easily-mp_sa_invoker" {
  members = [
    "allUsers",
    "serviceAccount:${local.service_account_email}",
  ]
  role     = "roles/run.invoker"
  service  = google_cloud_run_service.doit_easily_cloudrun_service.name
  location = var.cloudrun_location
  project  = var.project_id
}

#we need to do this for IAP in cloudrun https://cloud.google.com/iap/docs/identity-howto per https://cloud.google.com/iap/docs/enabling-cloud-run#before_you_begin

resource "google_secret_manager_secret" "settings_toml" {
  project = var.project_id
  secret_id = "settings-toml"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "settings_toml" {
  secret      = google_secret_manager_secret.settings_toml.id
  secret_data = file("${path.module}/custom-settings.toml")
}


resource "google_secret_manager_secret_iam_binding" "setting_toml_accessors" {
  secret_id = google_secret_manager_secret.settings_toml.id
  members = ["serviceAccount:${local.service_account_email}"]
  project = var.project_id
  role = "roles/secretmanager.secretAccessor"
}