# App Deploy Terraform

This module deploys doit-easily into cloudrun, including all required infrastucture

# iSaas Codelab vs Production
This terraform should be deployed once for the iSaaS Codelab (with the `TF_VAR_is_codelab=true`)
It should be deployed separately for a production version of Doit-easily (with the `TF_VAR_is_codelab` omitted (`false`))

Resources Created:
- pubsub subscription from Google Marketplace topic
- event topic (optional)
- cloud run service
- IAM policies