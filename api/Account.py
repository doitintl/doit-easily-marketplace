import os
from procurement_api import ProcurementApi
from middleware import logger

from config import settings


def handle_account(account_msg: dict, procurement_api: ProcurementApi):
    """Handles incoming Pub/Sub messages about account resources."""

    account_id = account_msg["id"]

    account = procurement_api.get_account(account_id)
    logger.debug("got account", account=account)
    if account and settings.private_offers_only:
            approval = None
            for account_approval in account["approvals"]:
                if account_approval["name"] == "signup":
                    approval = account_approval
                    break
            logger.debug("found approval", approval=approval)

            if approval:
                if approval["state"] == "PENDING":
                    logger.debug("approving account in procurementApi")
                    procurement_api.approve_account(account_id)

                elif approval["state"] == "APPROVED":
                    logger.info("account is already approved, no action performed")
            else:
                logger.debug("no approval found")
                # The account has been deleted