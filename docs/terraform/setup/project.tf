
resource "google_project" "isv-public" {
  name       = var.project_id
  project_id = var.project_id
  folder_id = var.folder_id
  billing_account = var.billing_id
}

