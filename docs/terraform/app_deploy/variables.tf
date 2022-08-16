variable "event_topic_name" {
  description = "(optional) The name of the event-topic to publish events to. This is the topic the ISV listens on to know when to create their infra. Env variable for cloud run service"
  default = ""
}

variable "cloudrun_location" {
  description = "The location to deploy location based services."
  default = "us-west1"
}

variable "doit_easily_version" {
  description = "The version of doit-easily to deploy"
}
variable "slack_webhook" {
  default = ""
  description = "(optional) Env variable for cloud run service. The slack hook to send event notifications to (new entitlement requests only)"
}
variable "is_codelab" {
  default = false
  description = "Env variable for cloud run service. Flag to run in codelab mode. Enables approving accounts because codelab has no frontend integration"
}
variable "marketplace_project" {
  description = "Env variable for cloud run service. The project id where your listing resides (and marketplace subscription)"
}
variable "backend_project" {
  default = ""
  description = "Env variable for cloud run service. The project this backend runs in. Can be the same as the MARKETPLACE_PROJECT"
}
variable "subscription_id" {
  default = ""
  description = "Env variable for cloud run service. The id of the subscription to listen on in processor mode (in GKE or pulling messages)"
}
variable "auto_approve_entitlements" {
  default = false
  description = "Env variable for cloud run service. Causes the processor to automatically approve entitlement creation requests"
}
variable "enable_push_endpoint" {
  default = false
  description = "Env variable for cloud run service. Causes the processor to enable the pubsub endpoint for push subscriptions"
}
variable "log_level" {
  default = "info"
  description = "Env variable for cloud run service. The log level"
}
variable "audience" {
#  default = "info"
  description = "Env variable for cloud run service. The audience for JWT validation"
}

variable "project_id" {
  type = string
  description = "The project ID to deploy this solution into"
}

variable "region" {
  description = "Location for load balancer and Cloud Run resources"
  type        = string
}

variable "ssl" {
  description = "Run load balancer on HTTPS and provision managed certificate with provided `domain`."
  type        = bool
  default     = true
}

variable "domain" {
  description = "Domain name to run the load balancer on. Used if `ssl` is `true`."
  type        = string
}

variable "lb_name" {
  description = "Name for load balancer and associated resources"
  type        = string
}

variable "enable_logging" {
    description = "Whether or not to enable logging on the api loadbalancer"
    type = bool
    default = false
}

variable "log_sample_rate" {
  description = "This field can only be specified if logging is enabled for this backend service. This configures the sampling rate of requests to the load balancer"
  type = number
  default = 0
}



variable "brand_name" {
  description = "The name of the oauth brand"
}

variable "project_number" {
  description = "The project number"
}

variable "brand_support_email" {
  description = "The email for oauth support"
}

variable "iap_client_display_name" {
  description = "The display name of the oauth client"
}

variable "managed_zone_name" {
  description = "The name of the managed zone to insert an A record"
}

variable "external_ip_name" {
  description = "The name of the external IP resource"
}

locals {
  demo_prefix = var.is_codelab ? "DEMO-" : ""
  topic = "projects/cloudcommerceproc-prod/topics/${local.demo_prefix}${var.marketplace_project}"
  project_id = var.backend_project == "" ? var.marketplace_project : var.backend_project
  #  this module only handles a single installation, so either codelab SA or the one we created before....
  service_account_id = var.is_codelab ? "saas-codelab" : "doit-easily"
  codelab_suffix = var.is_codelab ? "-codelab" : ""
}