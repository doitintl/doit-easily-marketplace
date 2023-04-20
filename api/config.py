from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DOITEZ",
    env_switcher="DOITEZ_ENV",
    envvar="DOITEZ_SETTINGS_FILE",
    # settings_files = Load these files in the order.
    settings_files=["default_settings.toml", "/config/custom-settings.toml"],
    environments=True,
    env="default",
)

settings.validators.register(
    # By default, this validator will raise an error if not explicitly set.
    # TODO: Should we default it to the current running project? (from metadata service)
    Validator("marketplace_project", must_exist=True, is_type_of=str),
    # the domain that hosts your product, such as `example-pro.com`
    Validator("audience", must_exist=True, is_type_of=str),
    Validator("auto_approve_entitlements", must_exist=True, is_type_of=bool),
    # optional. If set, slack notifications will be sent.
    Validator("slack_webhook", eq=None) | Validator("slack_webhook", is_type_of=str),
    # optional. If set, google pubsub will be used.
    Validator("event_topic", eq=None) | Validator("event_topic", is_type_of=str),
    # not optional. If set, codelab mode is enabled.
    Validator("is_codelab", must_exist=True, is_type_of=bool),
)

settings.validators.validate_all()
