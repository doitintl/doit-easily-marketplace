resource "google_project_service_identity" "iap_gsi" {
  provider = google-beta
  service = "iap.googleapis.com"
}

# This can be applied only once
resource "google_iap_brand" "iap_brand" {
  application_title = var.brand_name
  # The user/service account running the terraform has to have ownership over the email account in Google Groups.
  # To workaround this, if it's intended only for internal use, one may decide to use the email attached to that service account.
  support_email     = var.brand_support_email
  project           = var.project_number
}

resource "google_iap_client" "iap_client" {
  display_name = var.iap_client_display_name
  brand        =  google_iap_brand.iap_brand.name  
}