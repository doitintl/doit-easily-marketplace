import base64
import json


def pubsub_msg_from_dict(d):
    data = base64.b64encode(json.dumps(d).encode("utf-8")).decode("utf-8")
    return {"message": {"data": data}}


entitlement_states = [
    "ENTITLEMENT_ACTIVATION_REQUESTED",
    "ENTITLEMENT_ACTIVE",
    "ENTITLEMENT_PENDING_PLAN_CHANGE_APPROVAL",
    "ENTITLEMENT_ACTIVE",
    "ENTITLEMENT_CANCELLED",
]


def get_entitlement_response(state, product = "foo"):
    if state not in entitlement_states:
        raise f"state must be one of {entitlement_states}"

    return {
        "product": f"{product}.endpoints.doit-public.cloud.goog",
        "usageReportingId": "project_number:625643682501",
        "id": "b8273d26-21f1-4402-bedb-28f351ea9822",
        "createTime": "2022-07-18T09:39:24.803455Z",
        "account": "providers/doit-public/accounts/eda2a6ce-2e2d-44ff-985f-37e6c51af7d1",
        "provider": "doit-public",
        "name": "providers/doit-public/entitlements/b8273d26-21f1-4402-bedb-28f351ea9822",
        "updateTime": "2022-07-18T09:41:17.971091Z",
        "plan": "flexsave",
        "productExternalName": f"{product}.endpoints.doit-public.cloud.goog",
        "state": state
    }


def get_approved_account_response():
    return {
        "account": "providers/doit-public/accounts/eda2a6ce-2e2d-44ff-985f-37e6c51af7d1",
        "state": "ACCOUNT_ACTIVE",
        "approvals": [
            {                
                "name": "signup",
                "state": "APPROVED"
}
        ]
    }

def get_pending_account_response():
    return {
        "account": "providers/doit-public/accounts/eda2a6ce-2e2d-44ff-985f-37e6c51af7d1",
        "state": "ACCOUNT_ACTIVE",
        "approvals": [
            {
                "name": "signup",
                "state": "PENDING"
             }
        ]
    }


entitlement_event_states = [
    "ENTITLEMENT_CREATION_REQUESTED",
    "ENTITLEMENT_ACTIVE",
    "ENTITLEMENT_PLAN_CHANGE_REQUESTED",
    "ENTITLEMENT_PLAN_CHANGED",
    "ENTITLEMENT_PLAN_CHANGE_CANCELLED",
    "ENTITLEMENT_CANCELLED",
    "ENTITLEMENT_PENDING_CANCELLATION",
    "ENTITLEMENT_CANCELLATION_REVERTED",
    "ENTITLEMENT_DELETED"]


def get_pubsub_event_data(state):
    if state not in entitlement_event_states:
        raise f"state must be one of {entitlement_event_states}"

    return {
        "eventId": f"{state}-709a3d39-d3a3-4a2c-a8c8-4d508db342f5",
        "eventType": state,
        "entitlement": {
            "id": "c91aecd0-de62-43fc-88fd-ab0b77c57c7c",
            "updateTime": "2022-07-18T09: 42: 51.275760Z"
        },
        "providerId": "doit-public"
    }
