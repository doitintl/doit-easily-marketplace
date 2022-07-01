# Install Doit Easily in Cloud Run
This process is designed to be the distilled instructions found [here](3), plus instructions to deploy Doit-Easily

## The Process
1. Create a project to hold your listings and backend integration workloads. The project name should be in the format `<PARTNER_NAME>-public`

    ```
    export COMPANY_NAME=your company name
    gcloud projects create $COMPANY_NAME-public
    ```

2. Grant the following roles for Google access
```
    gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
    --member="user:cloud-commerce-marketplace-onboarding@twosync-src.google.com" \
    --role=roles/editor

    gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
    --member="user:cloud-commerce-marketplace-onboarding@twosync-src.google.com" \
    --role=roles/servicemanagement.admin

    gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
    --member="user:cloud-commerce-procurement@system.gserviceaccount.com" \
    --role=roles/servicemanagement.serviceConsumer

    gcloud projects add-iam-policy-binding $COMPANY_NAME-public \
    --member="user:cloud-commerce-procurement@system.gserviceaccount.com" \
    --role=roles/servicemanagement.serviceController
```
3. Submit your product information using this [Google Form](1)
4. Create a new SaaS listing in the [Producer Portal](2)
4. Start the process of submitting pricing & product information. This can be done in parallel to the technical integration
5. Create a service account to run your integration workloads

```
gcloud iam service-accounts create doit-easily \
    --description="Doit Easily backend integration" \
    --display-name="doit-easily" \
    --project=$COMPANY_NAME-public
```
6. Add the service account to the Technical Integration -> Billing Integration for both the Procurement API and Pub/Sub integrations
7. Copy the Pub/Sub topic string for later user. It should be in the format `projects/cloudcommerceproc-prod/topics/PARTNER_NAME-public`
1. create a slack webhook and record the URL
8. Deploy the backend integration in Cloud Run (and accompanying infrastructure)
    2. create a topic for notification events
    1. deploy the backend integration into cloud run (must run as the service account)
    1. create a subscription on the topic from the previous step using the backend integration URL for the push endpoint
    1. deploy the backend UI into cloud run
    1. deploy the frontend UI into cloud run
9. Add the frontend integration public URL to the Technical Integration -> Frontend Integration `Sign up URL`
    1. optional, use a custom domain by setting up a loadbalancer in front of cloudrun
    1. optional, add the SSO Login URL
9. 


TODO:
- [] add links to the latest image versions for all images
    * backend
    * backend ui
    * frontend
- [] add code samples or screenshots for all steps


[1]: https://docs.google.com/forms/d/e/1FAIpQLSfddn4mwKnqtLNQ-m7IgRZ-bgTz4BOsrEDWCf3XBjc_ogKNnA/viewform
[2]: https://console.cloud.google.com/producer-portal
[3]: https://cloud.google.com/marketplace/docs/partners/integrated-saas#checklist