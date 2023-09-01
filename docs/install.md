# Install Doit-Easily

This process is the distilled instructions found [here][3], plus information to deploy Doit-Easily.


1. [Pre-requisites](guide/1-pre-requisites.md)
1. [setup the listing](guide/2-setup-the-listing.md)
1. [deploy app](guide/3-deploy-app.md)
1. [test the deployment](guide/4-test-deployment.md)
1. [publish](guide/5-publish-listing.md)

## App Configuration
Describe the Toml file and how to configure the app

## FAQ

See the [faq](faq.md)

## Testing

See the [testing doc](testing.md)




**Terraform modules**

There are two Terraform modules in this directory: `setup` and `app_deploy`. They correspond with installation steps below.

You can apply the modules using either one of the following methods:

- Adding a `.tfvars` file with appropriately configured variables to directly apply the entire modules.

- Copying the pertinent files to your own terraform modules and apply them there.

We recommend the first approach, using the requested variables.



[1]: https://docs.google.com/forms/d/e/1FAIpQLSfddn4mwKnqtLNQ-m7IgRZ-bgTz4BOsrEDWCf3XBjc_ogKNnA/viewform
[2]: https://console.cloud.google.com/producer-portal
[3]: https://cloud.google.com/marketplace/docs/partners/integrated-saas#checklist
[5]: install-cloudrun.md
[6]: terraform/setup
[7]: gcloud/setup
[8]: terraform/app_deploy
[9]: terraform/setup/iam.tf
[10]: testing.md
[11]: terraform/app_deploy/README.md
[12]: ../api/README.md
