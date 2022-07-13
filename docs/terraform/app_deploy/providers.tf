provider "google-beta" {
  project = local.project_id
}
provider "google" {
  project = local.project_id
}


#get an access token for the doit-easily SA
data "google_service_account_access_token" "prod_token" {
  target_service_account = data.google_service_account.doit_easily_backend_integration_sa.email
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "1200s"
}

#this provider is used to apply resources as the doit-easily SA
provider "google" {
  alias        = "prod_impersonation"
  access_token = data.google_service_account_access_token.prod_token.access_token
}


