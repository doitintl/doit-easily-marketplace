import os
from flask import Flask, request

app = Flask(__name__)
project_id = os.getenv("MARKETPLACE_PROJECT")
assert project_id


@app.route("/activate", methods=["POST"])
def activate():
    user_jwt = request.headers.get("x-gcp-marketplace-token")
    print(user_jwt)
    """
    jwt = {
      "iss": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com",
      "iat": CURRENT_TIME,
      "exp": CURRENT_TIME + 5 minutes,
      "aud": "PARTNER_DOMAIN_NAME",
      "sub": "PROCUREMENT_ACCOUNT_ID",
      "google": {
        "roles": [GCP_ROLE],
        "user_identity": USER_ID
      }
    }

    need do this:
    When you receive the JWT, you must verify the following:
        Verify that the JWT signature is using the public key from Google.
        Verify that the JWT has not expired, by checking the exp claim.
        Verify that the aud claim is the correct domain for your product.
        Verify that the iss claim is https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com.
        Verify that sub is not empty.
        
    call the "backend-api.marketplace.svc.cluster.local/account/approve" endpoint to approve the procurement account
    
    also, sso?: https://cloud.google.com/marketplace/docs/partners/integrated-saas/frontend-integration#integrate-sso
    """
    pass


@app.route("/")
def index():
    try:
        return "", 200
    except Exception:
        return {"error": "Loading failed"}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
