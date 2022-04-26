export GCP_PROJECT_ID="doit-public"
export GCP_BACKEND_PROJECT_ID="doit-easily-dev"
export K8S_NAMESPACE="marketplace"
export SERVICE_ACCOUNT_ID="saas-codelab" # change to more generic name
export KEY_FILE=mp-sa-key.json
export TOPIC_NAME="projects/cloudcommerceproc-prod/topics/DEMO-doit-public" # TODO: make generic

# Run this after Google has granted permissions to the marketplace-sa

# allow the current user to operate as the marketplace-sa so they can create a pubsub subscription
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT_ID}@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
    --role roles/iam.serviceAccountTokenCreator \
    --member "user:$(gcloud auth list --filter=status:ACTIVE --format="value(account)")" \
    --project "${GCP_PROJECT_ID}"
gcloud pubsub subscriptions create ${GCP_BACKEND_PROJECT_ID} \
    --topic=${TOPIC_NAME} \
    --impersonate-service-account ${SERVICE_ACCOUNT_ID}@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
    --project "${GCP_PROJECT_ID}"