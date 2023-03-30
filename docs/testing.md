# Testing your listing
To test your listing you should create a direct billing account and project associated to the billing account. This BA and project should only be used for testing your listing. 

After you've created the BA, you need to register it with Google so that any charges are refunded. You need to have the role `roles/billing.admin` on the BA to subscribe to your listing

## Register a billing account for testing your listing
1. In the producer portal, select "Reports" in the left menu
2. Under "Configure Test Billing Accounts" click "ADD TEST BILLING ACCOUNT"
3. Add your billing account ID for a *direct* billing account (not your doit reseller account)

## Subscribing to your listing
1. In the Producer Portal, click on your listing
2. Select "Full Preview" and wait for the new tab to load
3. On the listing preview, change projects to the test project you created before
4. Choose a pricing model and subscribe to your listing

## Testing the JWT validation flow
1. In the Producer Portal, click on your listing
2. Select "Full Preview" and wait for the new tab to load
3. On the listing preview, change projects to the test project you created before
4. If this is the first time you're subscribing the JWT flow will happen automatically
5. If you've previously subscribed and created the procurement acccount you can test the JWT flow by doing the following:  
    a. Add your frontend integration URL to the SSO login field (See step `1.ii` from `Finish and Test Your Integration`)  
    b. After subscribing to the listing, test the JWT validation flow by clicking "Manage on Provider" from the "Full Preview"  
