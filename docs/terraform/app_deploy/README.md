# App Deploy Terraform

This module deploys doit-easily into cloudrun, including all required infrastucture  
Before applying this module, the [setup module][1] must be applied (or equivilent resources applied)

## What this Terraform deploys

TODO: a diagram showing all components deployed

The `app_deploy` terraform module will install & configure the following components/features:

* Deploy the backend integration into Cloud Run (must run as the service account `doit-easily` created previously).

* Create a push subscription on the topic `projects/cloudcommerceproc-prod/topics/ISV-public`, using the Cloud Run backend integration URL for the push endpoint.

* Deploy the backend UI into Cloud Run (optional if `AUTO_APPROVE_ENTITLEMENTS` is set to `true`).

* Deploy the frontend UI into Cloud Run (optional, you can also deploy your own frontend integration).

* Enable authentication for the backend (IAP).

* Create a default secret `settings-toml` which contains a default config


# Important Notes About the module

### You need an existing DNS zone
This terraform assumes you have a DNS zone already created. See [loadbalancer.tf](../docs/terraform/app_deploy/loadbalancer.tf) (line 3). If you need a new zone created, you'll need to modify the terraform to create the zone rather than reference one that exists.

### You need to update the secret setting-toml

This module creates a secret in Secret Manager named [settings-toml](../app_deploy/app.tf#L58) which is mounted to your Cloud Run service. The secret contains [initial](./custom-settings.toml) _default values_ which must be updated for DoiT-Easily to run correctly.

You must either:

*  put your secrets in the [custom-settings.toml](./custom-settings.toml) before applying the terraform 
*  after applying the terraform initially, manually update the secret in Secret Manager and then update the [secret_version](./example.tfvars#L2) in your tfvar file

### Granting users access to the backend UI

users need to be granted the `IAP-secured Web App User` role on the [IAP console](https://console.cloud.google.com/security/iap)


# Terraform Variable Descriptions

|variable | example value | description|
|--|--|--|
|doit_eaily_image|your-repo/doit-easily:1.0|the full path of your image with version|
|secret_version | 1 | the version of your Secret Manager secret|
|cloudrun_location | us-central1 | where to deploy your cloudrun service|
|is_codelab | false | flag to control the operation mode of doit-easily (deprecated)|
|project_id | your-project-id | project id of your marketplace project|
|project_number | 12345 | project number of your marketplace project|
|log_level | info | log level of the cloud run service|
|domain | you.website.example.com | the domain for the Load Balancer|
|region | us-central1 | the region for the Load Balancer Serverless NEG (should match the `cloudrun_location`)|
|ssl | true | flag to enable/disable SSL on the Load Balancer|
|lb_name | your-load-balancer | name for the load balancer in GCP console|
|enable_logging | false | flag to enable/disable load balancer logging|
|log_sample_rate | 0 | load balancer backend logging rate|
|brand_name | ISV - Marketplace | the name of the brand for the Oauth client|
|brand_support_email | you@isv.com | the contact email for the Oauth client|
|iap_client_display_name | ISV - Public | the display name for the Oauth client|
|managed_zone_name | existing dns zone name | the name of an existing Manged Zone in GCP|
|managed_zone_project | existing dns zone project name | the project id of the Managed Zone in GCP|
|external_ip_name | your-project-id-public-ip | the name for the IP address used for the Load Balancer|
|topic_name | topic-name-created-by-google | the name of the topic as defined in the Producer Portal (created by Google)|


# iSaas Codelab vs Production
|This terraform should be deployed once for the iSaaS Codelab (with the `TF_VAR_is_codelab|true`) | desc|
It should be deployed separately for a production version of Doit-easily (with the `TF_VAR_is_codelab` omitted (`false`))



[1]: ../setup/