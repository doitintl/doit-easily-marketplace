export GCP_PROJECT_ID="isv-public"
export GCP_BACKEND_PROJECT_ID="isv-public"
export K8S_NAMESPACE="marketplace"
export SERVICE_ACCOUNT_ID="saas-codelab" # change to more generic name
export KEY_FILE=mp-sa-key.json
export TOPIC_NAME="projects/cloudcommerceproc-prod/topics/DEMO-isv-public"

gcloud iam service-accounts create ${SERVICE_ACCOUNT_ID} \
    --description="marketplace backend integration" \
    --project "${GCP_PROJECT_ID}"

# GKE workload identity binding
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT_ID}@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:${GCP_BACKEND_PROJECT_ID}.svc.id.goog[${K8S_NAMESPACE}/mp-ksa]" \
    --project "${GCP_PROJECT_ID}"


#allow the marketplace-sa to managed pubsub in the isv-public project
gcloud project add-iam-policy-binding ${GCP_PROJECT_ID} \
    --role "roles/pubsub.editor" \
    --member "${SERVICE_ACCOUNT_ID}@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
    --project "${GCP_PROJECT_ID}"
