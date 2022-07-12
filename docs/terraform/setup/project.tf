
resource "google_project" "isv-public" {
  name       = local.project_id
  project_id = local.project_id
  folder_id = var.folder_id
}

