import os
from procurement_api import ProcurementApi
from middleware import logger

from config import settings


def handle_account(account_msg: dict, procurement_api: ProcurementApi):
    """Handles incoming Pub/Sub messages about account resources."""

    account_id = account_msg["id"]

    account = procurement_api.get_account(account_id)
    logger.debug("got account", account=account)
