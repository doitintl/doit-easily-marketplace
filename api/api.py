import base64
import os
import json
import uuid
from flask import request, Flask, render_template
from middleware import logger, add_request_context_to_log
import traceback

from procurement_api import ProcurementApi, is_account_approved
from Account import handle_account
from Entitlement import handle_entitlement

from config import settings
from google.cloud import pubsub_v1
import jwt, requests
from cryptography.x509 import load_pem_x509_certificate

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
        add_request_context_to_log(str(uuid.uuid4()))
        state = request.args.get('state', "ACTIVATION_REQUESTED")
        page_context = {}
        logger.debug("loading index")
        state = request.args.get("state", "ACTIVATION_REQUESTED")
        if state not in entitlement_states:
            entitlement_response = procurement_api.list_entitlements()
        else:
            entitlement_response = procurement_api.list_entitlements(state=state)
        logger.debug("entitlements loaded", entitlements=entitlement_response)
        page_context["entitlements"] = list(
            entitlement_response['entitlements']) if 'entitlements' in entitlement_response else []

        return render_template("index.html", **page_context)
    except Exception as e:
        logger.error(e)
        return {"error": "Loading failed"}, 500

@app.route(f"/app/account/<account_id>")
def show_account(account_id):
    try:
        add_request_context_to_log(str(uuid.uuid4()))
        page_context = {}
        logger.debug("loading account page")

        if account_id is None:
            page_context = {"error": "no account id provided"}
        account = procurement_api.get_account(account_id)

        if not account:
            page_context = {"error": "account not found"}

        page_context["account"] = account
        page_context["account"]["is_approved"] = is_account_approved(account)

        return render_template("account.html", **page_context)
    except Exception as e:
        logger.error(e)
        return {"error": "Loading failed"}, 500 

@app.route("/login", methods=["POST"])
@app.route("/activate", methods=["POST"])
def login():
    add_request_context_to_log(str(uuid.uuid4()))
    encoded = request.form.get("x-gcp-marketplace-token")
    logger.debug('encoded token', token=encoded)
    if not encoded:
        return "invalid header", 401
    header = jwt.get_unverified_header(encoded)
    key_id = header["kid"]
    # only to get the iss value
    unverified_decoded = jwt.decode(encoded, options={"verify_signature": False})
    url = unverified_decoded["iss"]

    # Verify that the iss claim is https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com.
    if url != "https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com":
        logger.error('oh no! bad public key url')
        return "", 401

    # get the cert from the iss url, and resolve it to a public key
    certs = requests.get(url=url).json()
    cert = certs[key_id]
    cert_obj = load_pem_x509_certificate(bytes(cert, 'utf-8'))
    public_key = cert_obj.public_key()

    # Verify that the JWT signature is using the public key from Google.
    try:
        decoded = jwt.decode(encoded, public_key, algorithms=["RS256"], audience=settings.AUDIENCE, )
    except jwt.exceptions.InvalidAudienceError:
        #     Verify that the aud claim is the correct domain for your product.
        logger.error('oh no! audience mismatch')
        return "audience mismatch", 401
    except jwt.exceptions.ExpiredSignatureError:
        #  Verify that the JWT has not expired, by checking the exp claim.
        logger.error('oh no! jwt expired')
        return "JWT expired", 401

    # Verify that sub is not empty.
    if decoded["sub"] is None or decoded["sub"] == "":
        logger.error('oh no! sub is empty')
        return "sub empty", 401

    # JWT validated, approve account
    logger.debug('approving account', account=decoded["sub"])
    try:
        response = procurement_api.approve_account(decoded["sub"])
        logger.info("procurement api approve complete", response={})
        if settings.auto_approve_entitlements:
            # look for any pending entitlement creation requests and approve them
            pending_creation_requests = procurement_api.list_entitlements(account_id=decoded["sub"])
            logger.debug("pending requests", pending_creation_requests=pending_creation_requests)
            for pcr in pending_creation_requests["entitlements"]:
                logger.debug("pending creation request", pcr=pcr)
                entitlement_id = procurement_api.get_entitlement_id(pcr["name"])
                logger.info("approving entitlement", entitlement_id=entitlement_id)
                procurement_api.approve_entitlement(entitlement_id)
        return "Your account has been approved. You can close this window.", 200
    except Exception as e:
        logger.error("an exception occurred approving accounts", exception=traceback.format_exc())
        return {"error": "failed to approve account"}, 500


# curl localhost:5000/v1/entitlement?state=CREATION_REQUESTED|ACTIVE|PLAN_CHANGE_REQUESTED|PLAN_CHANGED|PLAN_CHANGE_CANCELLED|CANCELLED|PENDING_CANCELLATION|CANCELLATION_REVERTED|DELETED
@app.route("/v1/entitlements", methods=["GET"])
def index():
    add_request_context_to_log(str(uuid.uuid4()))
    try:
        state = request.args.get("state", "ACTIVATION_REQUESTED")
        if state not in entitlement_states:
            return procurement_api.list_entitlements()
        else:
            return procurement_api.list_entitlements(state=state)
    except Exception:
        logger.error("an exception occurred listing entitlements", exception=traceback.format_exc())
        return {"error": "Procurement API call failed"}, 500


# curl --request POST localhost:5000/v1/entitlement/49849f71-849b-49ad-9c0f-60389c1604e5/approve  --header "Content-Type: application/json"
@app.route("/v1/entitlement/<entitlement_id>/approve", methods=["POST"])
def entitlement_approve(entitlement_id):
    add_request_context_to_log(str(uuid.uuid4()))
    logger.info("approve entitlement")
    try:
        procurement_api.approve_entitlement(entitlement_id)
        return "{}", 200
    except Exception as e:
        logger.error("an exception occurred approving entitlement", exception=traceback.format_exc())
        return {"error": "approve failed"}, 500


# curl --request POST localhost:5000/v1/entitlement/49849f71-849b-49ad-9c0f-60389c1604e5/reject --data '{"reason":"reason for rejection"}' --header "Content-Type: application/json"
@app.route("/v1/entitlement/<entitlement_id>/reject", methods=["POST"])
def entitlement_reject(entitlement_id):
    add_request_context_to_log(str(uuid.uuid4()))
    logger.info("reject entitlement")
    try:
        msg_json = request.json
        procurement_api.reject_entitlement(
            entitlement_id, msg_json["reason"]
        )
        return "{}", 200
    except Exception as e:
        logger.error("an exception occurred rejecting entitlement", exception=traceback.format_exc())
        return {"error": "reject failed"}, 500


# curl --request POST localhost:5000/v1/account/49849f71-849b-49ad-9c0f-60389c1604e5/approve --header "Content-Type: application/json"
@app.route("/v1/account/<account_id>/approve", methods=["POST"])
def account_approve(account_id):
    add_request_context_to_log(str(uuid.uuid4()))
    logger.info("approve account")
    try:
        response = procurement_api.approve_account(account_id)
        logger.info("procurement api approve complete", response=response)
        return "{}", 200
    except Exception as e:
        logger.error("an exception occurred approving account", exception=traceback.format_exc())
        return {"error": "approve failed"}, 500


# curl --request POST localhost:5000/v1/account/49849f71-849b-49ad-9c0f-60389c1604e5/reset --header "Content-Type: application/json"
@app.route("/v1/account/<account_id>/reset", methods=["POST"])
def account_reset(account_id):
    add_request_context_to_log(str(uuid.uuid4()))
    logger.info("reset account")
    try:
        response = procurement_api.reset_account(account_id)
        logger.info("procurement api reset complete", response=response)
        return "{}", 200
    except Exception as e:
        logger.error("exception resetting account", exception=traceback.format_exc())
        return {"error": "approve failed"}, 500


# A notification handler route that decodes messages from Pub/Sub
@app.route("/v1/notification", methods=["POST"])
def handle_subscription_message():
    add_request_context_to_log(str(uuid.uuid4()))
    logger.debug("event received")
    try:
        envelope = request.json
        if not envelope:
            logger.warn("no Pub/Sub message received")
            return "{}", 200

        if not isinstance(envelope, dict) or "message" not in envelope:
            logger.warn("invalid Pub/Sub message format")
            return "{}", 200

        message = envelope["message"]
        if isinstance(message, dict) and "data" in message:
            try:
                # decode b64, decode utf-8, strip, json parse
                message_json = json.loads(base64.b64decode(message["data"]).decode("utf-8").strip())
            except Exception as e:
                logger.debug("failure getting data", exception=e)
                return "{}", 200
            logger.debug("message_json", message_json=message_json)
        else:
            logger.warn("no JSON in message")
            return "{}", 200

        if "entitlement" in message_json:
            # handle the entitlement message
            handle_entitlement(
                message_json["entitlement"],
                message_json["eventType"],
                procurement_api,
                settings,
                publisher,
            )
        elif "account" in message_json:
            handle_account(message_json["account"], procurement_api)
        else:
            logger.warn("no account or entitlement in message")

        return "{}", 200
    except Exception as e:
        logger.error("an exception occurred", exception=traceback.format_exc())
        return "{}", 200


@app.route("/alive")
def alive():
    return "", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
