# Get the managed DNS zone

data "google_dns_managed_zone" "dns_zone" {
  name     = var.managed_zone_name
  project = var.managed_zone_project
}

resource "google_compute_global_address" "external_ip" {
  name     = var.external_ip_name
}
# Add the IP to the DNS
resource "google_dns_record_set" "api" {
  name         = "${var.domain}."
  type         = "A"
  ttl          = 300
  managed_zone = data.google_dns_managed_zone.dns_zone.name
  rrdatas      = [google_compute_global_address.external_ip.address]
}

resource "google_compute_url_map" "url_map" {
  name            = "api-lb-url-map"
  default_service = module.api-lb.backend_services["default"].self_link
  host_rule {
    hosts        = ["*"]
    path_matcher = "allpaths"
  }
  path_matcher {
    name = "allpaths"
    default_service = module.api-lb.backend_services["default"].self_link
    path_rule {
      paths   = ["/activate", "/login"]
      service = module.api-lb.backend_services["frontend"].self_link
    }
  }
}

module "api-lb" {
  source  = "GoogleCloudPlatform/lb-http/google//modules/serverless_negs"
  version = "~> 6.3"
  name    = "api-lb"
  project = var.project_id

  ssl                             = true
  managed_ssl_certificate_domains = [var.domain]
  https_redirect                  = true
#  labels                          = { "example-label" = "cloud-run-example" }
  url_map                         = google_compute_url_map.url_map.self_link
  create_url_map = false
  address                         = google_compute_global_address.external_ip.address
  create_address                  = false
  backends = {
    default = {
      description = null
      groups = [
        {
          group = google_compute_region_network_endpoint_group.api_lb_neg.id
        }
      ]
      enable_cdn              = false
      security_policy         = null
      custom_request_headers  = null
      custom_response_headers = null

      iap_config = {
        enable               = true
        oauth2_client_id     = google_iap_client.iap_client.client_id
        oauth2_client_secret = google_iap_client.iap_client.secret
      }
      log_config = {
        enable      = true
        sample_rate = 1
      }
    }

    frontend = {
      description = "public endpoint for frontend integration"
      groups      = [
        {
          group = google_compute_region_network_endpoint_group.api_lb_neg.id
        }
      ]
      enable_cdn              = false
      security_policy         = null
      custom_request_headers  = null
      custom_response_headers = null
      iap_config              = {
        enable               = false
        oauth2_client_id     = ""
        oauth2_client_secret = ""
      }
      log_config = {
        enable      = true
        sample_rate = 1
      }
    }
  }
}

resource "google_compute_region_network_endpoint_group" "api_lb_neg" {
  provider              = google-beta
  name                  = "api-lb-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = google_cloud_run_service.doit_easily_cloudrun_service.name
  }
}