# Install Doit Easily
This process is designed to be the distilled instructions found [here][3], plus instructions to deploy Doit-Easily

## Notes on the terraform modules
There are two complete Terraform modules in this directory, `setup` and `app_deploy`. These modules correspond with installation
steps below. You can directly apply these entire modules by adding a `.tfvars` file with appropriate variables configured. 
Or you can copy the pertinent files to your own terraform modules and apply them that way. I recommend still using the requested
variables.

## The Process to install Doit-Easily

### Setup
Note: These steps can be accomplished by applying this [Terraform][6] or [gcloud][7]
1. Create a project to hold your listings and backend integration workloads. The project name should be in the format `ISV-public`.
3. Grant Google procurement user access to your listing project
4. Create a service account to run your integration workloads

### Create a listing and start submitting details
Note: The following steps are completed in your web browser and Producer Portal 

3. Submit your product information using this [Google Form][1]  
4. Create a new SaaS listing in the [Producer Portal][2]  
5. Start the process of submitting pricing & product information. This can be done in parallel to the technical integration  
6. In the Producer Portal (see screenshot below)   
   1. link the service account to call the Procurement API and Cloud Pub/Sub Integration  
   2. copy the Pub/Sub topic string for later user.   
       It should be in the format `projects/cloudcommerceproc-prod/topics/ISV-public`  

![Diagram](../img/proc-api-screen-cap.png)

9. (optional) In Slack, create a slack webhook store this secret in Secret Manager.

### App Deploy 
Note: Note: These steps can be accomplished by applying this [Terraform][8] 
8. Deploy the application in Cloud Run. When finished, continue below

### Finish and test the integration
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
- [] TODO: are we going to give gcloud AND terraform instructions? can we pick one?

NOTE: we're ending up with a matrix of install instructions, its turning into a lot of documenation and we should pick one or two!

| | GKE | Cloud Run |
|--|--|--|
|Gcloud | | 
|Terraform | | 

[1]: https://docs.google.com/forms/d/e/1FAIpQLSfddn4mwKnqtLNQ-m7IgRZ-bgTz4BOsrEDWCf3XBjc_ogKNnA/viewform
[2]: https://console.cloud.google.com/producer-portal
[3]: https://cloud.google.com/marketplace/docs/partners/integrated-saas#checklist
[4]: install-gke.md
[5]: install-cloudrun.md
[6]: terraform/setup
[7]: gcloud/setup
[8]: terraform/app_deploy
