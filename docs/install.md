# DoiT-Easily Installation Guide


## Terraform modules

There are  Terraform modules here, under `docs/terraform`, to be used at the steps stated below.

You can apply the modules using either one of the following methods:

- Adding a `.tfvars` file with appropriately configured variables to directly apply the entire modules.
- Copying the pertinent files to your own terraform modules and apply them there.

How you incorporate these files into your CICD system is up to you. While we strive to not make breaking changes the Terraform modules, we can't promise we won't.

## The Install Process

This process is the distilled instructions found [here][3], plus information to deploy Doit-Easily.


1. [pre-requisites](guide/1-pre-requisites.md); use Terraform `docs/terraform/setup`.
1. [setup the listing](guide/2-setup-the-listing.md)
1. [deploy app](guide/3-deploy-app.md); use Terraform `docs/terraform/app_deploy`.
1. [test the deployment](guide/4-test-deployment.md)
1. [publish](guide/5-publish-listing.md)

## FAQ

See the [faq](faq.md)

## Testing

See the [testing doc](testing.md)



[3]: https://cloud.google.com/marketplace/docs/partners/integrated-saas#checklist
[5]: install-cloudrun.md
[6]: terraform/setup
[7]: gcloud/setup
[8]: terraform/app_deploy
[9]: terraform/setup/iam.tf
[10]: testing.md
[11]: terraform/app_deploy/README.md
[12]: ../api/README.md
