# Install Doit Easily
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
6. In the Producer Portal, add the service account to the Technical Integration -> Billing Integration page for both the Procurement API and Pub/Sub integrations.
7. In the Producer Portal, copy the Pub/Sub topic string for later user.   
    It should be in the format `projects/cloudcommerceproc-prod/topics/PARTNER_NAME-public`
1. In Slack, create a slack webhook store this secret in Secret Manager.
2. Create a topic for notification events (optional)
```
gcloud pubsub topics create saas-events --project=$COMPANY_NAME-public
```
8. Deploy the application in [GKE](4) or in [Cloud Run](5). When finished, continue here

10. In the Producer Portal, add the frontend integration URL to the Technical Integration -> Frontend Integration `Sign up URL`
     1. optional, use a custom domain by setting up a loadbalancer in front of cloudrun
     1. optional, add the SSO Login URL for your console, and support SSO
11. Test the solution by viewing the "Full Preview" from the listing in the producer portal. You can subscribe to the solution from this preview. 
12. Submit the product details, pricing details, and technical integration for review by Google
13. Publish your listing


TODO:
- [] add links to the latest image versions for all images
    * backend
    * backend ui
    * frontend
- [] add code samples or screenshots for all steps
- [] the backend-ui could be an SPA in a bucket rather than a cloud run service


[1]: https://docs.google.com/forms/d/e/1FAIpQLSfddn4mwKnqtLNQ-m7IgRZ-bgTz4BOsrEDWCf3XBjc_ogKNnA/viewform
[2]: https://console.cloud.google.com/producer-portal
[3]: https://cloud.google.com/marketplace/docs/partners/integrated-saas#checklist
[4]: install-gke.md
[5]: install.md