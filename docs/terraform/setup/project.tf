variable "isv_name" {
  description = "The name of the isv. All lower, no punctuation."
  validation {
    condition = can(regex("^[a-z][a-z0-9]*$", var.isv_name)) && length(var.isv_name) > 1
    error_message = "Must start with a letter, be all lower case and contain only letters and numbers."
  }
}

resource google_project isv-public {
  name       = "${var.isv_name}-public"
  project_id = "${var.isv_name}-public"
}

resource "google_project_iam_member" "cloud-commerce-marketplace-onboarding_editor" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-marketplace-onboarding@twosync-src.google.com"
  role    = "roles/editor"
}

resource "google_project_iam_member" "cloud-commerce-marketplace_admin" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-marketplace-onboarding@twosync-src.google.com"
  role    = "roles/servicemanagement.admin"
}

resource "google_project_iam_member" "cloud-commerce-procurement_serviceConsumer" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-procurement@system.gserviceaccount.com"
  role    = "roles/servicemanagement.serviceConsumer"
}

resource "google_project_iam_member" "cloud-commerce-procurement_serviceController" {
  project = google_project.isv-public.id
  member  = "user:cloud-commerce-procurement@system.gserviceaccount.com"
  role    = "roles/servicemanagement.serviceController"
}