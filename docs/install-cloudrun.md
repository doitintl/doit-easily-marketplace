# Install the app into Cloud Run

The `app_deploy` terraform module installs the following features
* deploy the backend integration into cloud run (must run as the service account `doit-easily` created previously)  
* create a push subscription on the topic `projects/cloudcommerceproc-prod/topics/ISV-public`, using the cloud run backend integration URL for the push endpoint  
* deploy the backend UI into cloud run (optional if `AUTO_APPROVE_ENTITLEMENTS` is set true)  
* deploy the frontend UI into cloud run (optional, you can deploy your own frontend integration if you want)
* enable authentication for the backend (IAP)