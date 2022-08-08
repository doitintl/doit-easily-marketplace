# Install the backend into an existing cluster

In short, create a `.tfvars` file with appropriate variables and apply the `app_deploy` terraform module.


9. Deploy the backend integration in Cloud Run (and accompanying infrastructure) (TODO: add cloud run button)
    1. deploy the backend integration into cloud run (must run as the service account `doit-easily` created previously)
    2. create a push subscription on the topic `projects/cloudcommerceproc-prod/topics/PARTNER_NAME-public`, using the cloud run backend integration URL for the push endpoint
    3. deploy the backend UI into cloud run (optional if `AUTO_APPROVE_ENTITLEMENTS` is set true)
    4. deploy the frontend UI into cloud run (optional, you can deploy your own frontend integration if you want)