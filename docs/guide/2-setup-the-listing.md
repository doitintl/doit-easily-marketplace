# Setup the listing

The following steps are completed in your web browser and Producer Portal.

1. Submit your product information using this [Google Form][1].

1. Once the Producer Portal is enabled, continue beyond this step

1. Create a new SaaS listing in the [Producer Portal][2]. 

1. Start the process of submitting pricing & product information. This can be done in parallel to the technical integration.  

1. In the Producer Portal (see screen capture below):

   1. Link the service account to call the Procurement API and Cloud Pub/Sub Integration.

   1. Copy the Pub/Sub topic string for later users.
       Use the format `projects/cloudcommerceproc-prod/topics/ISV-public`.
      
    ![Diagram](../../img/proc-api-screen-cap.png)  

1. (Optional) In Slack, create a Slack webhook to store this secret in Secret Manager.


# Next Steps

[deploy app](3-deploy-app.md)


[1]: https://docs.google.com/forms/d/e/1FAIpQLSfddn4mwKnqtLNQ-m7IgRZ-bgTz4BOsrEDWCf3XBjc_ogKNnA/viewform
[2]: https://console.cloud.google.com/producer-portal