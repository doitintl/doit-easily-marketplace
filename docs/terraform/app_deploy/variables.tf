variable "event_topic_name" {
  description = "(optional) The name of the event-topic to publish events to. This is the topic the ISV listens on to know when to create their infra. Env variable for cloud run service"
  default = ""
}

variable "cloudrun_location" {
  description = "The location to deploy location based services."
  default = "us-west1"
}

variable "doit_easily_image" {
  description = "The image path of doit-easily to deploy"
}
variable "slack_webhook" {
  default = ""
  description = "(optional) Env variable for cloud run service. The slack hook to send event notifications to (new entitlement requests only)"
}
variable "is_codelab" {
  default = false
  description = "Env variable for cloud run service. Flag to run in codelab mode. Enables approving accounts because codelab has no frontend integration"
}
variable "project_id" {
  description = "Env variable for cloud run service. The project id where your listing resides (and marketplace subscription)"
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
  description = "Env variable for cloud run service. The audience for JWT validation. Should be the domain portion of your URL"
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

variable "managed_zone_project" {
  description = "The project id of the managed zone"
}

variable "external_ip_name" {
  description = "The name of the external IP resource"
}

variable "topic_name" {
  default=""
  description = "IF your topic name does not match your project name, you can set it here"
}

locals {
  demo_prefix = var.is_codelab ? "DEMO-" : ""
  topic = "projects/cloudcommerceproc-prod/topics/${local.demo_prefix}${var.topic_name != "" ? var.topic_name : var.project_id}"
  #  this module only handles a single installation, so either codelab SA or the one we created before....
  service_account_email = var.is_codelab ? "saas-codelab@${var.project_id}.iam.gserviceaccount.com" : "doit-easily@${var.project_id}.iam.gserviceaccount.com"
  codelab_suffix = var.is_codelab ? "-codelab" : ""
}