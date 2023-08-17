# App Deploy Terraform

This module deploys doit-easily into cloudrun, including all required infrastucture  
Before applying this module, the [setup module][1] must be applied (or equivilent resources applied)

# iSaas Codelab vs Production
This terraform should be deployed once for the iSaaS Codelab (with the `TF_VAR_is_codelab=true`)
It should be deployed separately for a production version of Doit-easily (with the `TF_VAR_is_codelab` omitted (`false`))

Resources Created:
- pubsub subscription from Google Marketplace topic
- event topic (optional)
- cloud run service
- IAM policies
- Load balancer, backend, managed SSL cert, A record


### Pre-requisites to applying this terraform

Before running this terraform verify the following:

* The user or service account that runs this terraform needs to have `serviceAccountTokenCreator` on the `doit-easily` SA created in the setup terraform
* Build and publish the application image to GCR or Artifact Registry. See the API [README][1] for instructions. If you don't have an existing registry, you need to create one. 
* grant the Cloud Run Service Agent pull access to the registry where your doit-easily image is published
* The [TOML formatted configuration](../../../api/README.md#configuration) is stored in the [provided custom-settings.toml file, which contains valid settings keys with blank values (and must be customized to contain values that are valid for your deployment, before deploying)](./custom-settings.toml)


### Terraform Variables

doit_easily_image = "your-repo/doit-easily:1.0"
secret_version = "1"
cloudrun_location = "us-central1"
is_codelab = false
project_id = "your-project-id"
log_level = "info"
audience = "you.website.example.com"
region = "us-central1"
ssl = true
domain = "you.website.example.com"
lb_name = "doit-test-davec-load-balancer"
enable_logging = false
log_sample_rate = 0
brand_name = "DoiT Dave Test - Marketplace"
project_number = 12345
brand_support_email = "dave.c@doit-intl.com"
iap_client_display_name = "DoiT Dave Test - Public"
managed_zone_name = "doit-easily-cavaletto-dev"
managed_zone_project = "your-project-id"
external_ip_name = "your-project-id-public-ip"
topic_name = "doit-test-dave-public"

### After deploying the app
* grant users access to log into the backend UI via IAP
* update the secret `settings-toml` with valid values


[1]: ../setup/