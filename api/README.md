# Doit-Easily

Application repo for Doit-Easily. A simple python app for interacting with the Procurement API and Marketplace Topic messages.

# Build and publish the image
From the api directory you can build and publish the app using the following command. You need to have a gcr or artifact registry to push the image to. Proper IAMs configurations are required to submit the build and publish the image.

    gcloud builds submit  --tag <registry path>/doit-easily:1.0  .

# Running the application locally

    cd api
    docker build . -t doit-easily:local 
    gcloud auth login --cred-file='path/to/SA_key.json' 
    gcloud auth application-default login --impersonate-service-account=doit-easily@doit-test-davec-public.iam.gserviceaccount.com
    docker run -e PORT=8080 -v ./default_settings.toml:/config/custom-settings.toml -e GOOGLE_APPLICATION_CREDENTIALS=/creds.json -v $GOOGLE_APPLICATION_CREDENTIALS:/creds.json -p 8080:8080 -e LOG_LEVEL=debug docker.io/library/doit-easily:local

# Configuration

NOTE: this configuration file is mounted via a Secret Manager secret, see this note in the  [deployment instructions](../docs/terraform/app_deploy/README.md#you-need-to-update-the-secret-setting-toml) and the [Terraform](../docs/terraform/app_deploy/app.tf#L19) 

The configuration is managed by [DynaConf](https://www.dynaconf.com) and should be configured in the following way:

A file in TOML format stores the configuration and it should be mount inside the container as a volume. The default location is `/config/custom-settings.toml`, but can be changed by setting the `DOITEZ_SETTINGS_FILE` environment variable.

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