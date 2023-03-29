import base64
import os
import unittest
from importlib import reload
from unittest import mock
from unittest.mock import patch

from util import pubsub_msg_from_dict, get_entitlement_response, get_approved_account_response, get_pubsub_event_data, get_pending_account_response

DEFAULT_ENV_VARS = {
    "INCLUDES_FOR_DYNACONF": "test/configs/test.toml"
}


class TestPubsub(unittest.TestCase):
    def test_alive_endpoint(self):
        with mock.patch.dict(os.environ, DEFAULT_ENV_VARS):
            import api
            reload(api)
            response = api.app.test_client().get('/alive')
            assert response.status_code == 200

    def test_notification_endpoint_errors(self):
        with mock.patch.dict(os.environ, DEFAULT_ENV_VARS):
            import api
            reload(api)
            response = api.app.test_client().post('/v1/notification')
            assert response.status_code == 200

            response = api.app.test_client().post('/v1/notification', json={"FOO": "BAR"})
            assert response.status_code == 200

            response = api.app.test_client().post('/v1/notification', json={"message": "BAR"})
            assert response.status_code == 200

            response = api.app.test_client().post('/v1/notification', json={"message": {}})
            assert response.status_code == 200

            response = api.app.test_client().post('/v1/notification', json={"message": {"data": "BAR"}})
            assert response.status_code == 200

            data = "a string"
            response = api.app.test_client().post('/v1/notification', json={
                "message": {"data": base64.b64encode(data.encode("utf-8")).decode("utf-8")}})
            assert response.status_code == 200

            data = {}
            response = api.app.test_client().post('/v1/notification',
                                                  json=pubsub_msg_from_dict(data))
            assert response.status_code == 200

    # This patches the environment with env vars
    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    def test_notification_entitlement_message(self):
        # You must import the api and reload it so the new env vars are picked up
        import api
        reload(api)

        # after the api module is reloaded, then you patch methods on the procurement api to mock the return values
        with patch("api.procurement_api.get_entitlement") as mocked_get_entitlement, \
            patch("api.procurement_api.get_account") as mocked_get_account:
            mocked_get_entitlement.return_value = get_entitlement_response("ENTITLEMENT_ACTIVATION_REQUESTED")
            mocked_get_account.return_value = get_approved_account_response()

            # the data from pubsub
            data = get_pubsub_event_data("ENTITLEMENT_CREATION_REQUESTED")

            response = api.app.test_client().post('/v1/notification', json=pubsub_msg_from_dict(data))
            assert response.status_code == 200

    # This patches the environment with env vars, setting specific keys for this test
    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    def test_notification_entitlement_message_auto_approve_enabled(self):
        import api
        reload(api)

        with patch("api.procurement_api.approve_entitlement") as mocked_approve_entitlement, \
            patch("api.procurement_api.get_entitlement") as mocked_get_entitlement, \
            patch("api.procurement_api.get_account") as mocked_get_account:
            mocked_get_entitlement.return_value = get_entitlement_response("ENTITLEMENT_ACTIVATION_REQUESTED", product="mock-auto-approve")
            mocked_get_account.return_value = get_approved_account_response()
            # mocked_approve_entitlement.return_value = "OK"
            # uncomment the next line to throw an exception
            # mocked_approve_entitlement.side_effect = Exception

            # the data from pubsub
            data = get_pubsub_event_data("ENTITLEMENT_CREATION_REQUESTED")

            response = api.app.test_client().post('/v1/notification', json=pubsub_msg_from_dict(data))
            assert response.status_code == 200
            assert mocked_approve_entitlement.called == True

    # This patches the environment with env vars, setting specific keys for this test
    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    def test_notification_entitlement_message_auto_approve_enabled_account_pending(self):
        import api
        reload(api)

        with patch("api.procurement_api.approve_entitlement") as mocked_approve_entitlement, \
            patch("api.procurement_api.get_entitlement") as mocked_get_entitlement, \
            patch("api.procurement_api.get_account") as mocked_get_account:
            mocked_get_entitlement.return_value = get_entitlement_response("ENTITLEMENT_ACTIVATION_REQUESTED", product="mock-auto-approve")
            mocked_get_account.return_value = get_pending_account_response()
            # mocked_approve_entitlement.return_value = "OK"
            # uncomment the next line to throw an exception
            # mocked_approve_entitlement.side_effect = Exception

            # the data from pubsub
            data = get_pubsub_event_data("ENTITLEMENT_CREATION_REQUESTED")

            response = api.app.test_client().post('/v1/notification', json=pubsub_msg_from_dict(data))
            assert response.status_code == 200
            # approve not called because account is pending
            assert mocked_approve_entitlement.called == False 
