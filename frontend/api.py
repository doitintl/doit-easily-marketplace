import os
from datetime import datetime
import requests
from cryptography.x509 import load_pem_x509_certificate
from flask import Flask, request
import jwt

app = Flask(__name__)

audience = os.getenv("AUDIENCE")
assert audience
backend_api_url = os.getenv("BACKEND_API_URL")
assert backend_api_url


@app.route("/fe/activate", methods=["POST"])
def activate():
    encoded = request.form.get("x-gcp-marketplace-token")
    print(f'encoded token {encoded}')
    if not encoded:
        return "invalid header", 401
    header = jwt.get_unverified_header(encoded)
    key_id = header["kid"]
    # only to get the iss value
    unverified_decoded = jwt.decode(encoded, options={"verify_signature": False})
    url = unverified_decoded["iss"]

    # Verify that the iss claim is https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com.
    if url != "https://www.googleapis.com/robot/v1/metadata/x509/cloud-commerce-partner@system.gserviceaccount.com":
        print('oh no! bad public key url')
        return "", 401

    # get the cert from the iss url, and resolve it to a public key
    certs = requests.get(url=url).json()
    cert = certs[key_id]
    cert_obj = load_pem_x509_certificate(bytes(cert, 'utf-8'))
    public_key = cert_obj.public_key()

    # Verify that the JWT signature is using the public key from Google.
    try:
        decoded = jwt.decode(encoded, public_key, algorithms=["RS256"], audience=audience, )
    except jwt.exceptions.InvalidAudienceError:
        #     Verify that the aud claim is the correct domain for your product.
        print('oh no! audience mismatch')
        return "audience mismatch", 401
    except jwt.exceptions.ExpiredSignatureError:
        #  Verify that the JWT has not expired, by checking the exp claim.
        print('oh no! jwt expired')
        return "JWT expired", 401

    # Verify that sub is not empty.
    if decoded["sub"] is None or decoded["sub"] == "":
        print('oh no! sub is empty')
        return "sub empty", 401

    # JWT validated, approve account
    print(f'approving account {decoded["sub"]}')
    response = requests.post(backend_api_url, json={"account_id": decoded["sub"]})
    if response.status_code == 200:
        print('woot')
        return "You're account has been approved. You can close this window.", 200
    else:
        print(f'uh-oh, status code is {response.status_code}, {response.text}')
        return response.text, response.status_code





@app.route("/")
def index():
    try:
        return "I'm alive", 200
    except Exception:
        return {"error": "Loading failed"}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
