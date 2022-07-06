# Frequently Asked Questions

* What if I have multiple listings? Do I need multiple projects?
    * All marketplace listings should reside in a single project. This means IAMs around viewing listings are managed at the project level and apply to all listings
* If I have multiple listings, how many topics does Google provide?
    * There is single topic for all saas listings.If you have multiple saas listings (products), then your backend integration would need to handle all saas integrations
* Can I put my backend integration into a different project than the "isv-public" project?
    * The policy `constraints/iam.disableCrossProjectServiceAccountUsage` can complicate things  if you want to host the backend in cloudrun (or other hosted compute). This policy prevents cross project service account usage, which is required if the compute lives in a project other than "isv-public" (which is where the service account resides)
* What if a customer needs to install my product into multiple clusters/projects?
    * The procurement account is tied to the billing account in a 1:1 relationship. An entitlement is tied to the procurement account. Once the procurement account is subscribed to the entitlement, they can install the product into any project associated with that billing account. A SaaS/GKE (sosa) app can be installed in any project/cluster that is tied to the billing account
* What is the sosa model?
  * SaaS licensing with a customer component. Often done as 2 listings, Saas and GKE. Customer pays for GKE workload costs and  saas costs for backend processing.
* How can I test my listing before releasing it?
  * Once the billing and product integrations are complete, fill out the technical integration
  * Click the Full Preview button to get your listing
  * Create a project in the same org as your listing project
    * you need billing admin for the billing account
* After "purchasing" the product in integration testing, how can I purchase it again?
  * use the account reset endpoint on the backend server to reset your account
  * the SA that runs your server needs billing admin permissions on the billing account
