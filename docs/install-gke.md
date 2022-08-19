# Install the backend into an existing cluster

## Application CRD 
If you cluster doesn't have the Application CRD, you'll need it. [Install the Application CRD][4] into the cluster  
`kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/application/master/deploy/kube-app-manager-aio.yaml`



1. Have the mpdev tool installed
2. Run the following script, updating variables as appropriate

```
    #!#!/usr/bin/env bash
    APP_INSTANCE_NAME="backend-integration"
    NAMESPACE="dev"
    IS_CODELAB="true"
    MARKETPLACE_PROJECT="ISV-public"
    BACKEND_PROJECT="ISV-public" # originally setup to run in separate projects, not doing this due to org policy issues
    LOG_LEVEL="debug"
    SLACK_WEBHOOK="REPLACE_WITH_A_REAL_SLACK_HOOK" # leave blank if not using
    EVENT_TOPIC="projects/ISV-public/topics/backend-integration-dev-events" # leave blank if not using
    SUBSCRIPTION_ID="projects/ISV-public/subscriptions/backend-integration-dev"
    GOOGLE_SERVICE_ACCOUNT_EMAIL="saas-codelab@ISV-public.iam.gserviceaccount.com"
    DEPLOYMENT_SERVICE_ACCOUNT="mp-ksa"

    # support running this as an executable
    TAG=${1:-"v0.0.0"}
    echo $TAG
    mpdev install  --deployer=gcr.io/doit-public/doit-easily/deployer:${TAG} --parameters="{\"app_instance_name\":\"${APP_INSTANCE_NAME}\",\"namespace\":\"${NAMESPACE}\",\"is_codelab\":${IS_CODELAB},\"marketplace_project\":\"${MARKETPLACE_PROJECT}\",\"backend_project\":\"${BACKEND_PROJECT}\",\"log_level\":\"${LOG_LEVEL}\",\"slack_webhook\":\"${SLACK_WEBHOOK}\",\"event_topic\":\"${EVENT_TOPIC}\",\"subscription_id\":\"${SUBSCRIPTION_ID}\",\"google_service_account_email\":\"${GOOGLE_SERVICE_ACCOUNT_EMAIL}\",\"deployment_service_account\":\"${DEPLOYMENT_SERVICE_ACCOUNT}\"}"
```
3. Verify the backend by curling the API
   1. list entitlements   
      `curl localhost:8080/entitlement`
   2. approve entitlement  
      `curl --request POST localhost:8080/entitlement/approve --data '{"entitlement_id":"some-id-from-prior-request"}' --header "Content-Type: application/json"`
