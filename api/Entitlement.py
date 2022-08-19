import json
import os
import sys
from unittest.mock import MagicMock
import requests
from google.pubsub_v1 import PublisherClient

from procurement_api import ProcurementApi
from middleware import logger

from dynaconf import Dynaconf

def notify(type, entitlement, event_topic, publisher):
    # TODO: in a SaaS model, this should call some service endpoint (provided via env) to create the service
    logger.info(
        "notify entitlement change",
        type=type,
        entitlement=entitlement,
        event_topic=event_topic,
    )
    try:
        if event_topic:
            data = json.dumps({"event": type, "entitlement": entitlement}).encode(
                "utf-8"
            )
            publisher.publish(event_topic, data)
        else:
            logger.warn("no event_topic configured, setup messages dropped")

        return True
    except Exception as e:
        logger.error("failed to publish to topic", topic=event_topic, error=e)
        return False


def send_slack_message(webhook_url, entitlement: dict):
    title = f"New Entitlement Creation Request"
    message = "A new entitlement creation request has been submitted"
    slack_data = {
        "text": title,
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title,
                },
            },
            {
                # "color": "#9733EE",
                "type": "section",
                "text": {"type": "mrkdwn", "text": json.dumps(entitlement, indent=4)},
            },
        ],
    }

    byte_length = str(sys.getsizeof(slack_data))
    headers = {"Content-Type": "application/json", "Content-Length": byte_length}
    response = requests.post(webhook_url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        logger.error(
            "failed to send message to slack",
            status_code=response.status_code,
            response_text=response.text,
        )
        # raise Exception(response.status_code, response.text)


# https://cloud.google.com/marketplace/docs/partners/integrated-saas/backend-integration#eventtypes
def handle_entitlement(
    event: dict,
    event_type: str,
    procurement_api: ProcurementApi,
    settings: Dynaconf,
    publisher: PublisherClient = None,
) -> bool:
    """Handles incoming Pub/Sub messages about entitlement resources."""
    logger.debug("handle_entitlement", event_dict=event, event_type=event_type)
    entitlement_id = event["id"]
    entitlement = procurement_api.get_entitlement(entitlement_id)
    entitlement["id"] = entitlement_id
    logger.debug(
        f"checked procurement api for entitlement",
        entitlement=entitlement,
        entitlement_id=entitlement_id,
    )

    if not entitlement:
        # Do nothing. The entitlement has to be canceled to be deleted, so
        # this has already been handled by a cancellation message.
        logger.debug("entitlement not found in procurement api, ack and do nothing")
        return True

    # Get the product name from the entitlement object
    product_name = entitlement["product"]
    logger.info("entitlement for", product_name=product_name)
    # Get the first substring from a split using . as the separator. Should be safe for prod and Codelab
    product_name = product_name.split(".")[0]
    # Load DynaConf settings for the product
    product_settings = settings.from_env(product_name)

    logger.debug('product config settings', 
                 product_name=product_name, 
                 event_topic=product_settings.event_topic, 
                 auto_approve_entitlements=product_settings.auto_approve_entitlements)

    account_id = procurement_api.get_account_id(entitlement["account"])
    account = procurement_api.get_account(account_id)
    if account["state"] != "ACCOUNT_ACTIVE":
        # The account is not active, wait for the account to be active
        # before processing this customers entitlement requests
        logger.debug(
            "customer is not ACTIVE, nack entitlement message",
            account_state=account["state"],
        )
        return False

    entitlement_state = entitlement["state"]
    logger.debug(f"entitlement state", state=entitlement_state)

    # NOTE: because we don't persist any of this info to a local DB, there isn't much to do in this app.
    if event_type == "ENTITLEMENT_CREATION_REQUESTED":
        if entitlement_state == "ENTITLEMENT_ACTIVATION_REQUESTED":
            logger.debug(f"HERE {product_settings.marketplace_project}")
            if product_settings.auto_approve_entitlements:
                logger.debug("auto approving entitlement")
                procurement_api.approve_entitlement(entitlement_id)

            # TODO: we could send an update to the customer giving an approval timeline
            #  https://cloud.google.com/marketplace/docs/partners/integrated-saas/backend-integration#sending_a_status_message_to_users

            if product_settings.slack_webhook:
                send_slack_message(product_settings.slack_webhook, entitlement)
            # Nothing to do here, as the approval comes from the UI
            return True

    elif event_type == "ENTITLEMENT_ACTIVE":
        if entitlement_state == "ENTITLEMENT_ACTIVE":
            return notify("create", entitlement, product_settings.event_topic, publisher)

    elif event_type == "ENTITLEMENT_PLAN_CHANGE_REQUESTED":
        if entitlement_state == "ENTITLEMENT_PENDING_PLAN_CHANGE_APPROVAL":
            # Don't write anything to our database until the entitlement
            # becomes active within the Procurement Service.
            procurement_api.approve_entitlement_plan_change(
                entitlement_id, entitlement["newPendingPlan"]
            )
            return True

    elif event_type == "ENTITLEMENT_PLAN_CHANGED":
        if entitlement_state == "ENTITLEMENT_ACTIVE":
            return notify("upgrade", entitlement, product_settings.event_topic, publisher)

    elif event_type == "ENTITLEMENT_PLAN_CHANGE_CANCELLED":
        # Do nothing. We approved the original change, but we never recorded
        # it or changed the service level since it hadn't taken effect yet.
        return True

    elif event_type == "ENTITLEMENT_CANCELLED":
        if entitlement_state == "ENTITLEMENT_CANCELLED":
            return notify("destroy", entitlement, product_settings.event_topic, publisher)

    elif event_type == "ENTITLEMENT_PENDING_CANCELLATION":
        # Do nothing. We want to cancel once it's truly canceled. For now
        # it's just set to not renew at the end of the billing cycle.
        return True

    elif event_type == "ENTITLEMENT_CANCELLATION_REVERTED":
        # Do nothing. The service was already active, but now it's set to
        # renew automatically at the end of the billing cycle.
        return True

    elif event_type == "ENTITLEMENT_DELETED":
        # Do nothing. The entitlement has to be canceled to be deleted, so
        # this has already been handled by a cancellation message.
        return True

    # TODO: handle ENTITLEMENT_OFFER_ENDED for private offers?
    #  Indicates that a customer's private offer has ended. The offer either triggers an ENTITLEMENT_CANCELLED event or remains active with non-discounted pricing.
    return False
