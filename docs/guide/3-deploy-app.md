# Deploy the App


1. Build and publish the image

   For detailed instructions see the [api readme](../../api/README.md)

1. Create a copy of the [example.tfvars](../terraform/app_deploy/example.tfvars) file and add your values.  

   For detailed instructions see this [README](../terraform/app_deploy/README.md)

1. Apply the Terraform

1. Update the secret in Secret Manager

1. Bump the secret version in tfvars and redeploy the service

1. In the Producer Portal, add the frontend integration URL to the Technical Integration -> Frontend Integration `Sign up URL`.

     1. (Optional.) Use a custom domain by setting up a load balancer in front of Cloud Run.

     2. (Optional.) Add the SSO Login URL for your console, and support SSO. OR link to your website and disable SSO

   ![Diagram](../../img/proc-url-screen-cap.png)









# Next Steps

[test the deployment](4-test-deployment.md)