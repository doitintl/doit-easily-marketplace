# Deploy the App

#### Please see the [README][11] for important instructions about deploying the app and its prerequisites.

1. Build and publish the application [image][12]

   cd api
   gcloud build submit ....

1. copy and update the example.tfvars file

1. Deploy the application and related infrastructure. When finished, continue below.

1. update the secret in Secret Manager

1. bump the secret version in tfvars and redeploy the service


Note: These steps can be accomplished by applying this [Terraform][8].

The `app_deploy` terraform module will install & configure the following components/features:

* Deploy the backend integration into Cloud Run (must run as the service account `doit-easily` created previously).

* Create a push subscription on the topic `projects/cloudcommerceproc-prod/topics/ISV-public`, using the Cloud Run backend integration URL for the push endpoint.

* Deploy the backend UI into Cloud Run (optional if `AUTO_APPROVE_ENTITLEMENTS` is set to `true`).

* Deploy the frontend UI into Cloud Run (optional, you can also deploy your own frontend integration).

* Enable authentication for the backend (IAP).

* Create a default secret `settings-toml` which contains a default config

## Important Notes About the Terraform

### DNS Zone
This terraform assumes you have a DNS zone already created. See [loadbalancer.tf](../docs/terraform/app_deploy/loadbalancer.tf) (line 3). If you need a new zone created, you'll need to modify the terraform to create the zone rather than reference one that exists.

### You need to update the secret setting-toml
Either put your secrets in the `terraform/docs/app_deploy/custom-settings.toml` before applying the terraform OR after applying the terraform initially, manually update the secret in Secret Manager and then update the secret_version in your tfvar file

# Next Steps

[test the deployment](4-test-deployment.md)