import os
import requests
from flask import Flask, request, render_template

API_URL = os.environ["API_URL"]
assert API_URL
URL_PREFIX = os.environ.get("URL_PREFIX", "")

# :embarassed: don't look at me, I'm ugly
# this is super hacky and lets us set the url prefix on the static js code. we should not do this.
# this entire app should become an SPA and the backend should the backend API rather than a separate server.
# for now this hack lets us set the url prefix to whatever the customer needs based on their ingress settings
with open("static/approve.js", 'r') as file:
    filedata = file.read()
filedata = filedata.replace('{URL_PREFIX}', URL_PREFIX)
with open("static/approve.js", 'w') as file:
    file.write(filedata)

app = Flask(__name__, static_folder="static", static_url_path=URL_PREFIX)


# assert URL_PREFIX starts with a /

def get_entitlements(state):
    try:
        query_string = f'?state={state}' if state else ''
        url = f"{API_URL}/entitlement{query_string}"
        print(f"url: {url}")
        response = requests.get(url)
        print(f"response: {response}")
        return response.json()
    except Exception as e:
        print(f'exception {e}')
        return []


# NOTE: we could just make this an SPA...then we don't need a server at all
@app.route(f"{URL_PREFIX}/entitlements")
def entitlements():
    try:
        state = request.args.get('state', "ACTIVATION_REQUESTED")
        page_context = {}
        print("loading index")
        entitlement_response = get_entitlements(state=state)
        print(f"entitlements: {entitlement_response}")
        page_context["entitlements"] = list(
            entitlement_response['entitlements']) if 'entitlements' in entitlement_response else []

        return render_template("noauth.html", **page_context)
    except Exception as e:
        print(e)
        return {"error": "Loading failed"}, 500


@app.route(f"{URL_PREFIX}/approve", methods=["POST"])
def approve():
    try:
        #     call the backend api /entitlement/approve endpoint
        msg_json = request.json
        response = requests.post(f"{API_URL}/entitlement/approve", json={"entitlement_id": msg_json['entitlement_id']})
        return {}, response.status_code
    except Exception as e:
        print(e)
        return {"error": "Loading failed"}, 500


@app.route(f"{URL_PREFIX}/reject", methods=["POST"])
def reject():
    try:
        #     call the backend api /entitlement/reject endpoint
        msg_json = request.json
        print(f"rejecting: {msg_json['entitlement_id']}")
        response = requests.post(f"{API_URL}/entitlement/reject",
                                 json={"entitlement_id": msg_json['entitlement_id'],
                                       "reason": msg_json["reason"]})
        print(f"response: {response}")
        return {}, response.status_code
    except Exception as e:
        print(e)
        return {"error": "Loading failed"}, 500


@app.route("/")
def index():
    try:
        return "I'm alive", 200
    except Exception:
        return {"error": "Loading failed"}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
