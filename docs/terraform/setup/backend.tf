terraform {
  backend "gcs" {
    bucket = "talonone-terraform-state"
    prefix = "terraform/marketplace"
  }
}