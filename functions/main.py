from flask import Flask, request, jsonify
from firebase_admin import credentials, auth, initialize_app
from firebase_functions import https_fn

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-key.json")
initialize_app(cred)

# Create a Flask app for HTTP-triggered functions
app = Flask(__name__)

@app.route("/setAdminRole", methods=["POST"])
def set_admin_role():
    try:
        # Get the data from the request
        data = request.get_json()
        if not data or "uid" not in data:
            return jsonify({"error": "UID is required"}), 400
        
        uid = data["uid"]

        # Set custom claims
        auth.set_custom_user_claims(uid, {"admin": True})

        return jsonify({"message": f"Successfully made user {uid} an admin."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/revokeAdminRole", methods=["POST"])
def revoke_admin_role():
    try:
        # Get the data from the request
        data = request.get_json()
        if not data or "uid" not in data:
            return jsonify({"error": "UID is required"}), 400
        
        uid = data["uid"]

        # Remove custom claims
        auth.set_custom_user_claims(uid, None)

        return jsonify({"message": f"Successfully removed admin role for user {uid}."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@https_fn.on_request()
def https_admin_users(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()