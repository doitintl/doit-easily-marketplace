# Pre-Requisites

## Terraform

This [Terraform](../terraform/setup/) module is used in the following.

## The Process

1. Create a Google Cloud project to hold your listings and backend integration workloads. The project ID must end in `-public`. It should make clear it is a marketplace project, so for example `my-isv-mp-public`.

1. `apply` the [Terraform](../terraform/setup/) module to grant Google procurement user access to your listing project ([role detail](../terraform/setup/iam.tf)). You will be asked for billing ID and for project ID (or you can pass in the variables for these).

1. Create a service account to run your integration workloads.

1. Verify that the user applying the Terraform for deploying the app has `serviceAccountTokenCreator` role on the `doit-easily` service account created in this step



# Next Steps

[setup the listing](2-setup-the-listing.md)
