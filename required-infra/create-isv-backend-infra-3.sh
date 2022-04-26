export GCP_PROJECT_ID="doit-easily-dev"
export NETWORK_NAME="mp-network"
export SUBNETWORK_NAME="mp-subnet"
export ROUTER_NAME="mp-router"
export NAT_NAME="mp-nat"
export NODES_RANGE="192.168.0.0/20"
export SERVICES_RANGE="10.0.32.0/20"
export PODS_RANGE="10.4.0.0/14"
export SERVICES_RANGE_NAME="mp-services"
export PODS_RANGE_NAME="mp-pods"
export REGION="us-central1"
export CLUSTER_NAME="mp-cluster1"
export AUTHORIZED_NETWORKS_RANGE="$(curl -s ifconfig.me)/32"
export EVENT_TOPIC_NAME="mp-create-events"

gcloud compute networks create ${NETWORK_NAME} \
    --subnet-mode custom \
    --project "${GCP_PROJECT_ID}"

gcloud compute networks subnets create ${SUBNETWORK_NAME} \
    --network ${NETWORK_NAME} \
    --region ${REGION} \
    --range ${NODES_RANGE} \
    --secondary-range ${PODS_RANGE_NAME}=${PODS_RANGE},${SERVICES_RANGE_NAME}=${SERVICES_RANGE} \
    --enable-private-ip-google-access\
    --project "${GCP_PROJECT_ID}"

gcloud compute routers create ${ROUTER_NAME} \
    --network ${NETWORK_NAME} \
    --region ${REGION}\
    --project "${GCP_PROJECT_ID}"

gcloud compute routers nats create ${NAT_NAME} \
    --region ${REGION} \
    --router ${ROUTER_NAME} \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips\
    --project "${GCP_PROJECT_ID}"

gcloud container clusters create-auto ${CLUSTER_NAME} \
    --region ${REGION} \
    --enable-master-authorized-networks \
    --master-authorized-networks ${AUTHORIZED_NETWORKS_RANGE} \
    --network ${NETWORK_NAME} \
    --subnetwork ${SUBNETWORK_NAME} \
    --scopes "https://www.googleapis.com/auth/cloud-platform" \
    --cluster-secondary-range-name ${PODS_RANGE_NAME} \
    --services-secondary-range-name ${SERVICES_RANGE_NAME} \
    --enable-private-nodes\
    --project "${GCP_PROJECT_ID}"

gcloud container clusters get-credentials ${CLUSTER_NAME} --region ${REGION} --project ${GCP_PROJECT_ID}

gcloud pubsub topics create ${EVENT_TOPIC_NAME} \
    --project "${GCP_PROJECT_ID}"

export GCP_BACKEND_PROJECT_ID="doit-easily-dev"
export SERVICE_ACCOUNT_ID="saas-codelab" # change to more generic name

gcloud pubsub topics add-iam-policy-binding ${EVENT_TOPIC_NAME} \
    --member "serviceAccount:${SERVICE_ACCOUNT_ID}@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
    --role "roles/pubsub.publisher" \
    --project "${GCP_BACKEND_PROJECT_ID}"
