# Frequently Asked Questions

## What if I have multiple listings? Do I need multiple projects?

Generally, all marketplace listings should reside in a single project. IAMs around viewing listings are managed at the project level and apply to all listings.

You can however have multiple listing projects if requirements dictate it is necessary.

## If I have multiple listings, how many topics does Google provide?

There is a single topic for all SaaS listings, per listing project. The topic name is the same as the project.

If you have multiple SaaS listings (products) in the same project, then your backend integration would need to handle all the SaaS integrations using the same topic.

## Can I put my backend integration into a project other than the "isv-public"?

Yes, however the policy `constraints/iam.disableCrossProjectServiceAccountUsage` could complicate things if you want to host the backend in Cloud Run (or other hosted compute).

This policy prevents cross project service account usage, which is required if the compute lives in a project other than "isv-public" (which is where the service account resides).

## What if a customer needs to install my product into multiple clusters/projects?

The procurement account is tied to the billing account in a 1:1 relationship. An entitlement is tied to the procurement account. Once the procurement account is subscribed to the entitlement, they can install the product into any project associated with that billing account. 

A SaaS/GKE (sosa) app can be installed in any project/cluster that is tied to the billing account.

## What is the sosa model?

Sosa model refers to a SaaS licensing with a customer component. Often done as two listings, SaaS and GKE. 

Customer pays for the GKE workload costs and SaaS costs for backend processing.

## How can I test my listing before releasing it?

Once the billing and product integrations are complete:

1. Fill out the technical integration.

1. Click the **Full Preview** button to get your listing.

1. Create a project in the same org as your listing project.

You need billing admin permission for the billing account.

## After "purchasing" the product in integration testing, how can I purchase it again?

To repurchase the product, use the account reset endpoint on the backend server to reset your account.

The SA that runs your server needs billing admin permissions on the billing account.

## I get the error "This method is not allowed for the requested URL" when I click "Manage on Provider" from my listing. What's going on?

The Login URL entered in the Frontend Integration is where the subscriber will be forwarded when they click "manage on provider" from the listing. 
 
How they will be forwarded is controlled by the "Enable SSO Login" radio button in the Technical Integration tab, Frontend Integration section
If Yes: they will be forwarded with a POST and a JWT per this [doc](https://cloud.google.com/marketplace/docs/partners/integrated-saas/frontend-integration#integrate-sso)  
If No: they will be forwarded with a GET  
 
Doit-Easily does not support a GET to the frontend integration. How you want to handle this scenario is up to you. You can enter your console URL in the Login URL field. Or enable SSO, and replace the frontend integration with a page which handles a POST, validates the JWT, and logs the user into your console.

## I cannot grant `cloud-commerce-procurement@system.gserviceaccount.com` the `roles/servicemanagement.serviceConsumer` or `roles/servicemanagement.serviceController` role. There are no service endpoints available.

Service Endpoints for Marketplace listings are created once a pricing draft is submitted for approval. To get past this step, grant `cloud-commerce-procurement@system.gserviceaccount.com` the `roles/servicemanagement.admin` role at the project level. This role covers both the `serviceConsumer` and `serviceController` roles.

