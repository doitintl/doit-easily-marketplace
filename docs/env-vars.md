# Environment Variables for the backend

|Variable Name|Platform|Description|  Example|
|--|--|---|--|
|APP_INSTANCE_NAME|GKE|The name for deployments/services/SAs/etc|backend-integration|
|DEPLOYMENT_SERVICE_ACCOUNT|GKE|The name of the Kubernetes SA running the app|"mp-ksa"|
|NAMESPACE|GKE|The namespace to run the app in| marketplace|
|BACKEND_PROJECT|GKE/Run|The project where the backend workload is running. Could be the same project as the MARKETPLACE_PROJECT|"ISV-public"|
|EVENT_TOPIC|GKE/Run|A topic name to enable notifications of entitlement events. Leave blank to disable notifications|projects/ISV-public/topics/backend-integration-dev-events|
|GOOGLE_SERVICE_ACCOUNT_EMAIL|GKE/Run|The service account added in the listing with permissions to the procurement API and pubsub topic |"saas-codelab@ISV-public.iam.gserviceaccount.com"|
|IS_CODELAB|GKE/Run|Flag indicating if the backend is running in "codelab mode"|true/false|
|LOG_LEVEL|GKE/Run|The log level|debug/info/error|
|MARKETPLACE_PROJECT|GKE/Run|The project where your listing exists. Could be the same project as the BACKEND_PROJECT. NOTE: This is technically the "provider ID" from the producer portal, which almost always matches the project ID.|"ISV-public"|
|SLACK_WEBHOOK|GKE/Run|A Slack webhook to enable notifications of new entitlement requests. Leave blank to disable notifications|todo|
|SUBSCRIPTION_ID|GKE/Run|The name of the subscription attached to Google's entitlement event topic|"projects/ISV-public/subscriptions/backend-integration-dev"|
