import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__, static_folder="static", static_url_path="/be")

API_URL = os.environ["API_URL"]
assert API_URL


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
@app.route("/be/entitlements")
def entitlements():
    try:
        state = request.args.get('state', "ACTIVATION_REQUESTED")
        page_context = {}
        print("loading index")
        entitlement_response = get_entitlements(state=state)
        print(f"entitlements: {entitlement_response}")
        page_context["entitlements"] = list(entitlement_response['entitlements']) if 'entitlements' in entitlement_response else []

        return render_template("noauth.html", **page_context)
    except Exception:
        return {"error": "Loading failed"}, 500


@app.route("/")
def index():
    try:
        return "I'm alive", 200
    except Exception:
        return {"error": "Loading failed"}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
