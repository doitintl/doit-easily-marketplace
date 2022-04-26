TODO  
- [ ] write docs for entire setup, referencing google marketplace docs as necessary
- [ ] create bash scripts that can be run
- [ ] example frontend integration
- [ ] manifests/infra to expose the backend UI using IAP
  - [ ] docs how to do it themselves
- [ ] docs about where we're leaving the services (UIs/authnz is left to customer)
- 


# marketplace setup steps from the get go
setup steps for the entire saas-codelab setup

exposing, the service, leave as cluster ip and give examples
do the service usage sidecar, but always report $0


# Required Infra
* kubernetes cluster (autopilot full private)
* saas-codelab SA 
* Marketplace Subscription


## Marketplace Subscription
Needs to run as the "marketplace-sa"
```
    cd required-infra/subscription
    terraform init
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/saas-codelab-sa-credential.json terraform apply
```

## IAM
Run as a regular CICD user
```
    cd required-infra/iam
    terraform init
    terraform apply
```





# Questions
* the saas-codelab-sa needs to create the subscription, it exists in the isv-public project.
  * where should we create the subscription? in the isv-public project? or in the backend project?
  * in isv-public
    * backend-sa needs consumeer access to isv-public subscription
  * in isv-backend
    * saas-codelab-sa needs pubsub editor access in isv-backend project