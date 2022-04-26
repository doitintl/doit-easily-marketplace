PROJECT=$(shell gcloud config get-value project | tr ':' '/')
REGISTRY=gcr.io/$(PROJECT)
TESTER_IMAGE=$(REGISTRY)/doit-easily/tester:$(TAG)
DEPLOYER_IMAGE=$(REGISTRY)/doit-easily/deployer:$(TAG)

TAG ?= 0.1

$(info ---- PROJECT = $(PROJECT))
$(info ---- REGISTRY = $(REGISTRY))
$(info ---- TAG = $(TAG))
$(info ---- TESTER_IMAGE = $(TESTER_IMAGE))
$(info ---- DEPLOYER_IMAGE = $(DEPLOYER_IMAGE))

# publish new images with `TAG=X.X make build`
.PHONY: build
build: deployer tester

.PHONY: deployer
deployer:
	docker build --build-arg TAG="$(TAG)" --build-arg REGISTRY="$(REGISTRY)/doit-easily" -f deployer/Dockerfile --tag $(DEPLOYER_IMAGE) . ;\
    docker push $(DEPLOYER_IMAGE) ;\


.PHONY: tester
tester:
	docker build -f apptest/tester/Dockerfile --tag $(TESTER_IMAGE) apptest/tester/ ;\
    docker push $(TESTER_IMAGE) ;\



.PHONY: verify
verify:
	mpdev verify --deployer=$(DEPLOYER_IMAGE) > verify.txt;\
