# Doit-Easily


Doit-Easily demonstrates the [backend integrations][1] required for a GCP marketplace SaaS Offering.

**Note: This solution is not an official product and is not supported by DoiT, but is a sample provided for your reference. Direct use of this code in production is discouraged, but you may fork, modify and run this code as needed (subject to the license).**

This application is heavily inspired by [gcp-marketplace-integrated-saas](https://github.com/googlecodelabs/gcp-marketplace-integrated-saas) repo

## Architectural diagram

![Diagram](img/simple-arch.png)

## Components

### GCP owned

* **marketplace listing**: The marketplace listing that your customers use to subscribe to your service. Used for public and private offers.

* **procurement api**: REST API to inform Google about entitlements and account statuses.

* **service api**: REST API to inform Google about usage for usage-based billing.

* **isv-public topic**: Pub/sub topic where Google publishes entitlement events (creation requested, update requested, etc.).

### ISV owned

* **frontend-integration**: The public website where customers are redirected to after subscribing to your listing. It conducts JWT validation and gives you an opportunity to collect additional customer information (for storing in your own DB).

* **backend-integration**: The service to receive and respond to entitlement events from Google. Provides a simplified API to interact with the procurement API.

* **isv-public subscription**: Subscription to the "isv-public topic".

* **isv provision service**: An optional service (not provided by this repository) that listens to events from the backend-integration. This service would provision resources in your backend for SaaS customers.

* **usage-reporter**: An optional service (only required for usage-based billing, not provided by this repository) that reports usage metrics to Google's Service API.

* **service account**: The doit-easily service account that runs your backend-integration. This service account has roles to interact with the procurement API and subscribe to the isv-public topic.

## Installation

This backend integration can be deployed as explained below.

### Cloud Run

See [Installation instructions](docs/install.md).


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
