# Environment Variables for the backend

|Variable Name|Platform|Description|  Example|
|--|--|---|--|
|APP_INSTANCE_NAME|GKE|The name for deployments/services/SAs/etc|backend-integration|
|NAMESPACE|GKE|The namespace to run the app in| marketplace|
|IS_CODELAB|GKE/Run|Flag indicating if the backend is running in "codelab mode"|true/false|
|MARKETPLACE_PROJECT|GKE/Run|The project where your listing exists. May be the same project as the BACKEND_PROJECT|"ISV-public"|
|BACKEND_PROJECT|GKE/Run|The project where the backend workload is running. May be the same project as the MARKETPLACE_PROJECT|"ISV-public"|
|LOG_LEVEL|GKE/Run|The log level|debug/info/error|
|SLACK_WEBHOOK|GKE/Run|A slack webhook to enable notifications of new entitlement requests. Leave blank to disable notifications|todo|
|EVENT_TOPIC|GKE/Run|A topic name to enable notifications of entitlement events. Leave blank to disable notifications|projects/ISV-public/topics/backend-integration-dev-events|
|SUBSCRIPTION_ID|GKE/Run|The name of the subscription attached to Google's entitlement event topic|"projects/ISV-public/subscriptions/backend-integration-dev"|
|GOOGLE_SERVICE_ACCOUNT_EMAIL|GKE/Run|The service account added in the listing with permissions to the procurement API and pubsub topic |"saas-codelab@ISV-public.iam.gserviceaccount.com"|
|DEPLOYMENT_SERVICE_ACCOUNT|GKE|The name of the Kubernetes SA running the app|"mp-ksa"|