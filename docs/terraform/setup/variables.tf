variable "project_id" {
  description = "The name of the isv marketplace project. All lower, numbers/hyphens allowed, must end in '-public'."
  validation {
    condition = can(regex("^[a-z][a-z0-9-]*-public$", var.isv_name)) && length(var.isv_name) > 1
    error_message = "Must start with a letter, be all lower case and contain only letters, numbers, and hyphens. Must end in '-public'."
  }
}

variable "folder_id" {
  description = "The numerical id of the folder to put this project in."
  default = ""
}