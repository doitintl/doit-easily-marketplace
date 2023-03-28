import os
from procurement_api import ProcurementApi
from middleware import logger

from config import settings

# https://cloud.google.com/marketplace/docs/partners/integrated-saas/backend-integration#create-account
def handle_account(account_msg: dict, procurement_api: ProcurementApi):
    """Handles incoming Pub/Sub messages about account resources."""

    account_id = account_msg["id"]

    account = procurement_api.get_account(account_id)
    logger.debug(f"got account", account=account)
    ############################## IMPORTANT ##############################
    ### In true integrations, Pub/Sub messages for new accounts should  ###
    ### be ignored. Account approvals are granted as a one-off action   ###
    ### during customer sign up. This codelab does not include the sign ###
    ### up flow, so it chooses to approve accounts here instead.        ###
    ### Production code for real, non-codelab services should never     ###
    ### blindly approve these. The following should be done as a result ###
    ### of a user signing up.                                           ###
    #######################################################################
    if account and settings.IS_CODELAB:
        approval = None
        for account_approval in account["approvals"]:
            if account_approval["name"] == "signup":
                approval = account_approval
                break
        logger.debug(f"found approval", approval=approval)

        if approval:
            if approval["state"] == "PENDING":
                # See above note. Actual production integrations should not
                # approve blindly when receiving a message.
                logger.debug("approving account in procurementApi")
                procurement_api.approve_account(account_id)

            elif approval["state"] == "APPROVED":
                logger.info("account is approved")
        else:
            logger.debug("no approval found")
            # The account has been deleted
