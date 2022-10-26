# Install the app into Cloud Run

The `app_deploy` terraform module will install & configure the following components/features:

* Deploy the backend integration into Cloud Run (must run as the service account `doit-easily` created previously).

* Create a push subscription on the topic `projects/cloudcommerceproc-prod/topics/ISV-public`, using the Cloud Run backend integration URL for the push endpoint.

* Deploy the backend UI into Cloud Run (optional if `AUTO_APPROVE_ENTITLEMENTS` is set to `true`).

* Deploy the frontend UI into Cloud Run (optional, you can also deploy your own frontend integration).

* Enable authentication for the backend (IAP).


## Important Notes About the Terraform

## DNS Zone
This terraform assumes you have a DNS zone already created. See [loadbalancer.tf](../docs/terraform/app_deploy/loadbalancer.tf) (line 3). If you need a new zone created, you'll need to modify the terraform to create the zone rather than reference one that exists.