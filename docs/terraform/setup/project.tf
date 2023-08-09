
resource "google_project" "isv-public" {
  name       = var.project_id
  project_id = var.project_id  
  billing_account = var.billing_id
  org_id = var.org_id
}

