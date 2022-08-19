# Doit-Easily

Application repo for Doit-Easily. A simple python app for interacting with the Procurement API and Marketplace Topic messages.
The application is a single docker image with two running modes, api & processor.

## Processor

In this running mode the app listens for messages on a pull subscription and processes the messages.

## API

In this running mode the app runs a Flask server and acts as a proxy for the Procurement API.

## Configuration

The configuration is managed by [DynaConf](https://www.dynaconf.com) and should be configured in the following way:

A file in TOML format stores the configuration and it should be mount inside the container as a volume. The default location is `/app/custom-settings.toml`, but can be changed by setting the `DOITEZ_SETTINGS_FILE` environment variable.

The configuration uses a layered system for multi environments:

- The `[default]` environment is the default environment and it defines the default values for all the other environments.
- For each specific Marketplace listing, an environment can be defined and it will override the default values. For example, for the "Flexsave-dev" listing, the environment `[flexsave-dev]` can be used to override the default values.

```toml
[default]
marketplace_project = "doit-public"       # This must be set otherwise an error will be thrown.
auto_approve_entitlements = false
# event_topic
# slack_webhook

[flexsave-dev]
event_topic = "projects/doitintl-cmp-flexsave-gcp-mp-a/topics/procurement"
slack_webhook = "https://hooks.slack.com/services/T0JQQQQQQQ/B0JQQQQQQQ/XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
auto_approve_entitlements = true
```

- MARKETPLACE_PROJECT - The project id where your listing resides (and marketplace subscription)
- AUTO_APPROVE_ENTITLEMENTS - Causes the processor to automatically approve entitlement creation requests
- SLACK_WEBHOOK - The slack hook to send event notifications to (new entitlement requests only)
- EVENT_TOPIC - The topic to publish create/update/delete events on. This is the topic the ISV listens on to know when to create their infra
- BACKEND_PROJECT - The project this backend runs in. Can be the same as the MARKETPLACE_PROJECT
- IS_CODELAB - Internal. Flag to run in codelab mode. Enables approving accounts because codelab has no frontend integration
- MOCK_PROCUREMENT - Internal. Flag to run in mock procurement mode.

# CICD

Image building & publishing done via Cloud Build triggers on tags created on any branch. See cloudbuild.yaml and
Cloud Build Console in the Doit-Public project.

# Local development

Running this app locally is a pain. So rather than do that, run it in GCP. A set of manifests can be found in the `k8s`
directory. You need a cluster with workload identity, and a subscription. Basically you run the codelab app.

# Related Repositories

- https://github.com/doitintl/doit-easily - application repo for Doit Easily.
- https://github.com/doitintl/doit-easily-marketplace - "public" repo showing how to deploy our GKE solution.
- https://github.com/doitintl/doit-easily-integration - "public" repo showing how to deploy additional integrations (frontend and backend-ui).
- https://github.com/doitintl/doit-easily-saas - private repo for deploying Doit-Easily backend integration.

Releasing a new version

1. build the docker image by tagging the repo
2. build the deployer by bumping the version in schema.yaml and tagging the repo
