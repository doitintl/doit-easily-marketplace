export VERSION=0.0.1-daveclocal
export IMAGE_NAME=backend-ui
export PROJECT=$(shell gcloud config get-value project | tr ':' '/')
export REGISTRY=gcr.io/$(PROJECT)
export APP_NAME=doit-easily

.PHONY: remote-build
remote-build:
	gcloud builds submit  --tag $$REGISTRY/$$APP_NAME/$$IMAGE_NAME:$$VERSION .

.PHONY: apply
apply:
	kubectl apply -k k8s/mp-customer