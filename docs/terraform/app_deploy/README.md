# App Deploy Terraform

This module deploys doit-easily into cloudrun, including all required infrastucture

# iSaas Codelab vs Production
This terraform should be deployed once for the iSaaS Codelab (with the `TF_VAR_is_codelab=true`)
It should be deployed separately for a production version of Doit-easily (with the `TF_VAR_is_codelab` omitted (`false`))

Resources Created:
- pubsub subscription from Google Marketplace topic
- event topic (optional)
- cloud run service
- IAM policies
- Load balancer, backend, managed SSL cert, A record

### Terraform Variables



### Pre-requisites

Before running this terraform verify the following:

* The user or service account that runs this terraform needs to have `serviceAccountTokenCreator` on the `doit-easily` SA created in the setup terraform
* Build and publish the application image to GCR or Artifact Registry. See the API [README][1] for instructions. If you don't have an existing registry, you need to create one. 
* grant the Cloud Run Service Agent pull access to the registry where your doit-easily image is published
* The [TOML formatted configuration](../../../api/README.md#configuration) is stored in the [provided blank custom-settings.toml file](./custom-settings.toml)


### After deploying the app
* grant users access to log into the backend UI via IAP