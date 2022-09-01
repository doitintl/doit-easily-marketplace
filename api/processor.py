import base64
import json
import os
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from Account import handle_account
from Entitlement import handle_entitlement
from procurement_api import ProcurementApi
from middleware import logger

MARKETPLACE_PROJECT = os.getenv("MARKETPLACE_PROJECT")
assert MARKETPLACE_PROJECT
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
assert SUBSCRIPTION_ID
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
EVENT_TOPIC = os.getenv("EVENT_TOPIC")

MOCK_PROCUREMENT = os.environ.get("MOCK_PROCUREMENT", "False").lower() == "true"
procurement_api = ProcurementApi(MARKETPLACE_PROJECT)

publisher = pubsub_v1.PublisherClient()

####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
# This file needs work, its broken as an entry point
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
def handle_subscription_message(message: Message) -> None:
    try:
        logger.debug("got message", data=message.data)
        message_json = json.loads(message.data.decode("utf-8").strip())
        logger.debug("message_json", message_json=message_json)
        should_ack = False

        if "entitlement" in message_json:
            # handle the entitlement message
            should_ack = handle_entitlement(
                message_json["entitlement"],
                message_json["eventType"],
                procurement_api,
                SLACK_WEBHOOK,
                EVENT_TOPIC,
                publisher,
            )
            logger.debug("should_ack", should_ack=should_ack)
        elif "account" in message_json:
            should_ack = handle_account(message_json["account"], procurement_api)
            logger.debug("should_ack", should_ack=should_ack)
        else:
            logger.warn("no account or entitlement in message")
            # this really shouldn't happen
            message.nack()

        if should_ack:
            message.ack()
            logger.debug("ack done")
        else:
            message.nack()
            logger.debug("nack done")
    except Exception as e:
        message.nack()
        logger.debug("exception nack done", exception=e)


subscriber = pubsub_v1.SubscriberClient()

# TODO: create th subscription


future = subscriber.subscribe(SUBSCRIPTION_ID, handle_subscription_message)
with subscriber:
    try:
        future.result()
    except TimeoutError:
        future.cancel()  # Trigger the shutdown.
        future.result()  # Block until the shutdown is complete.

# blocks the thread we're on

# to stop receiving messages (listen for shutdown and call this probably)
# future.cancel()
