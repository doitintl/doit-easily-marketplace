#!/usr/bin/env bash

export COMPANY_NAME="Put your company name here"

# Step 1
gcloud projects create $COMPANY_NAME-public

# Step 2
gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
--member="user:cloud-commerce-marketplace-onboarding@twosync-src.google.com" \
--role=roles/editor

gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
--member="user:cloud-commerce-marketplace-onboarding@twosync-src.google.com" \
--role=roles/servicemanagement.admin

# If those are failing see ../../faq.md
gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
--member="user:cloud-commerce-procurement@system.gserviceaccount.com" \
--role=roles/servicemanagement.serviceConsumer

gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
--member="user:cloud-commerce-procurement@system.gserviceaccount.com" \
--role=roles/servicemanagement.serviceController

# Step 3
gcloud iam service-accounts create doit-easily \
    --description="Doit Easily backend integration" \
    --display-name="doit-easily" \
    --project=$COMPANY_NAME-public