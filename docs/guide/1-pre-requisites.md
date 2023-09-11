# Pre-Requisites

Note: These steps can be accomplished by applying this [Terraform](../terraform/setup/).

1. Create a project to hold your listings and backend integration workloads. The project name should be in the format `ISV-public` or otherwise clear it is a marketplace project.

1. Grant Google procurement user access to your listing project ([role detail](../terraform/setup/iam.tf)).

1. Create a service account to run your integration workloads.

1. Verify that the user applying the app deploy terraform has `serviceAccountTokenCreator` role on the `doit-easily` SA created in this step



# Next Steps

[setup the listing](2-setup-the-listing.md)