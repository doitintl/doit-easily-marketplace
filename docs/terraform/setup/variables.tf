variable "isv_name" {
  description = "The name of the isv. All lower, no punctuation."
  validation {
    condition = can(regex("^[a-z][a-z0-9]*$", var.isv_name)) && length(var.isv_name) > 1
    error_message = "Must start with a letter, be all lower case and contain only letters and numbers."
  }
}

variable "folder_id" {
  description = "The numerical id of the folder to put this project in."
  default = ""
}

locals {
  project_id = "${var.isv_name}-public"
}