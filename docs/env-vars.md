# Environment Variables for the backend

|Variable Name|Platform|Description|  Example|
|--|--|---|--|
|APP_INSTANCE_NAME|GKE|The name for deployments/services/SAs/etc|backend-integration|
|DEPLOYMENT_SERVICE_ACCOUNT|GKE|The name of the Kubernetes SA running the app|"mp-ksa"|
|BACKEND_PROJECT|Run|The project where the backend workload is running. Could be the same project as the MARKETPLACE_PROJECT|"ISV-public"|
|EVENT_TOPIC|Run|A topic name to enable notifications of entitlement events. Leave blank to disable notifications|projects/ISV-public/topics/backend-integration-dev-events|
|GOOGLE_SERVICE_ACCOUNT_EMAIL|Run|The service account added in the listing with permissions to the procurement API and pubsub topic |"doit-easily@ISV-public.iam.gserviceaccount.com"|
|LOG_LEVEL|Run|The log level|debug/info/error|
|MARKETPLACE_PROJECT|Run|The project where your listing exists. Could be the same project as the BACKEND_PROJECT. NOTE: This is technically the "provider ID" from the producer portal, which almost always matches the project ID.|"ISV-public"|
|SLACK_WEBHOOK|Run|A Slack webhook to enable notifications of new entitlement requests. Leave blank to disable notifications|todo|
|SUBSCRIPTION_ID|Run|The name of the subscription attached to Google's entitlement event topic|"projects/ISV-public/subscriptions/backend-integration-dev"|
