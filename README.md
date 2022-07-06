# Overview

Doit-Easily is the [backend integrations][1] required for a GCP marketplace Saas Offering.

# Overview
![Diagram](img/simple-arch.png)

## Components

### GCP owned
* marketplace listing: The marketplace listing your customer's use to subscribe to your service. Used for public and private offers.
* procurement api: REST API to inform Google about entitlement and account statuses
* service api: REST API to inform Google about usage for usage based billing
* isv-public topic: pub/sub topic where Google publishes entitlment events (creation requested, update requested, etc)

### ISV owned
* frontend-integration: public website where customers are redirected after subscribing to your listing. Does JWT validation and gives you an opportunity to collect additional customer information (for storing in your own DB)
* backend-integration: service to receive and respond to entitlement events from Google. Provides a simplified API to interact with the procurement API
* isv-public subscription: subscription to the "isv-public topic"
* isv provision service: an optional service (not provided by this repository) which listens to events from the backend-integration. This service would provision resources in your backend for SaaS customers
* usage-reporter: an optional service (only required for usage based billing, not provided by this repository) which reports usage metrics to Google's Service API
* service account: the doit-easily service account which runs your backend-integration. This service account has roles to interact with the procurement API and subscribe to the isv-public topic.


This backend integration can be deployed in several ways. Into GKE, or into Cloud Run. We recommend Cloud Run.

## Installation into Cloud Run or GKE

See instructions [here](docs/install.md)

# local setup
Set it up in a cluster in gcp, easier to run as the SA (rather than suggesting DLing the json key and all that)
Deploy it with `IS_CODELAB=true` to run in codelab mode

## Application CRD 
If you cluster doesn't have the Application CRD, you'll need it. [Install the Application CRD][4] into the cluster  
`kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/application/master/deploy/kube-app-manager-aio.yaml`


[1]: https://cloud.google.com/marketplace/docs/partners/integrated-saas/backend-integration
[2]: https://cloud.google.com/marketplace/docs/partners/integrated-saas#checklist
[3]: https://codelabs.developers.google.com/codelabs/gcp-marketplace-integrated-saas/#0
[4]: https://cloud.google.com/solutions/using-gke-applications-page-cloud-console#preparing_gke
[5]: ./required-infra/3-create-isv-backend-infra.sh
[6]: ./required-infra/1-create-isv-public-infra.sh
[7]: ./required-infra/2-create-isv-public-infra.sh
[8]:https://cloud.google.com/marketplace/docs/partners/integrated-saas/technical-integration-setup
[9]: https://cloud.google.com/marketplace/docs/partners/integrated-saas/backend-integration#producer-portal-service-accounts
[10]: ./docs/install-mpdev.md