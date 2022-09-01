import base64
import os
import json
from flask import request, Flask, render_template
from middleware import logger

from procurement_api import ProcurementApi
from Account import handle_account
from Entitlement import handle_entitlement

from config import settings
from google.cloud import pubsub_v1

app = Flask(__name__)

publisher = pubsub_v1.PublisherClient()
procurement_api = ProcurementApi(settings.MARKETPLACE_PROJECT)

entitlement_states = [
    "CREATION_REQUESTED",
    "ACTIVE",
    "PLAN_CHANGE_REQUESTED",
    "PLAN_CHANGED",
    "PLAN_CHANGE_CANCELLED",
    "CANCELLED",
    "PENDING_CANCELLATION",
    "CANCELLATION_REVERTED",
    "DELETED",
]

# NOTE: we could just make this an SPA...then we don't need a server at all
@app.route(f"/app")
def entitlements():
    try:
        state = request.args.get('state', "ACTIVATION_REQUESTED")
        page_context = {}
        print("loading index")
        state = request.args.get("state", "ACTIVATION_REQUESTED")
        if state not in entitlement_states:
            entitlement_response = procurement_api.list_entitlements()
        else:
            entitlement_response = procurement_api.list_entitlements(state=state)
        print(f"entitlements: {entitlement_response}")
        page_context["entitlements"] = list(
            entitlement_response['entitlements']) if 'entitlements' in entitlement_response else []

        return render_template("index.html", **page_context)
    except Exception as e:
        print(e)
        return {"error": "Loading failed"}, 500


@app.route("/login", methods=["GET"])
def login():
    return {"Hello,": "world"}, 200


# curl localhost:5000/v1/entitlement?state=CREATION_REQUESTED|ACTIVE|PLAN_CHANGE_REQUESTED|PLAN_CHANGED|PLAN_CHANGE_CANCELLED|CANCELLED|PENDING_CANCELLATION|CANCELLATION_REVERTED|DELETED
@app.route("/v1/entitlements", methods=["GET"])
def index():
    logger.info("loading index")
    try:
        state = request.args.get("state", "ACTIVATION_REQUESTED")
        if state not in entitlement_states:
            return procurement_api.list_entitlements()
        else:
            return procurement_api.list_entitlements(state=state)
    except Exception:
        return {"error": "Procurement API call failed"}, 500


# curl --request POST localhost:5000/v1/entitlement/49849f71-849b-49ad-9c0f-60389c1604e5/approve  --header "Content-Type: application/json"
@app.route("/v1/entitlement/<entitlement_id>/approve", methods=["POST"])
def entitlement_approve(entitlement_id):
    logger.info("approve entitlement")
    try:
        procurement_api.approve_entitlement(entitlement_id)
        return "{}", 200
    except Exception as e:
        logger.error(e)
        return {"error": "approve failed"}, 500


# curl --request POST localhost:5000/v1/entitlement/49849f71-849b-49ad-9c0f-60389c1604e5/reject --data '{"reason":"reason for rejection"}' --header "Content-Type: application/json"
@app.route("/v1/entitlement/<entitlement_id>/reject", methods=["POST"])
def entitlement_reject(entitlement_id):
    logger.info("reject entitlement")
    try:
        msg_json = request.json
        procurement_api.reject_entitlement(
            entitlement_id, msg_json["reason"]
        )
        return "{}", 200
    except Exception as e:
        logger.error(e)
        return {"error": "reject failed"}, 500


# curl --request POST localhost:5000/v1/account/49849f71-849b-49ad-9c0f-60389c1604e5/approve --header "Content-Type: application/json"
@app.route("/v1/account/<account_id>/approve", methods=["POST"])
def account_approve(account_id):
    logger.info("approve account")
    try:
        response = procurement_api.approve_account(account_id)
        logger.info("procurement api approve complete", response=response)
        return "{}", 200
    except Exception as e:
        logger.error(e)
        return {"error": "approve failed"}, 500


# curl --request POST localhost:5000/v1/account/49849f71-849b-49ad-9c0f-60389c1604e5/reset --header "Content-Type: application/json"
@app.route("/v1/account/<account_id>/reset", methods=["POST"])
def account_reset(account_id):
    logger.info("reset account")
    try:
        response = procurement_api.reset_account(account_id)
        logger.info("procurement api reset complete", response=response)
        return "{}", 200
    except Exception as e:
        logger.error(e)
        return {"error": "approve failed"}, 500


# A notification handler route that decodes messages from Pub/Sub
@app.route("/v1/notification", methods=["POST"])
def handle_subscription_message():
    logger.warn("event received")
    try:
        envelope = request.json
        if not envelope:
            logger.warn("no Pub/Sub message received")
            return "{}", 400

        if not isinstance(envelope, dict) or "message" not in envelope:
            logger.warn("invalid Pub/Sub message format")
            return "{}", 400

        message = envelope["message"]
        if isinstance(message, dict) and "data" in message:
            try:
                # decode b64, decode utf-8, strip, json parse
                message_json = json.loads(base64.b64decode(message["data"]).decode("utf-8").strip())
            except Exception as e:
                logger.debug("failure getting data", exception=e)
                # returning a 400 because this means the request was malformed
                return "{}", 400
            logger.debug("message_json", message_json=message_json)
        else:
            logger.warn("no JSON in message")
            return "{}", 400

        if "entitlement" in message_json:
            # handle the entitlement message
            should_ack = handle_entitlement(
                message_json["entitlement"],
                message_json["eventType"],
                procurement_api,
                settings,
                publisher,
            )
            logger.debug("should_ack", should_ack=should_ack)
        elif "account" in message_json:
            should_ack = handle_account(message_json["account"], procurement_api)
            logger.debug("should_ack", should_ack=should_ack)
        else:
            logger.warn("no account or entitlement in message")
            # this really shouldn't happen
            return "{}", 400

        if should_ack:
            logger.debug("ack done")
            return "{}", 204
        else:
            logger.debug("nack done")
            return "{}", 500
    except Exception as e:
        logger.debug("exception nack done", exception=e)
        return "{}", 500


@app.route("/alive")
def alive():
    return "", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
