from flask import Flask, request, jsonify
from firebase_admin import credentials, auth, initialize_app
from firebase_functions import https_fn

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-key.json")
initialize_app(cred)

# Create a Flask app for HTTP-triggered functions
app = Flask(__name__)


# Middleware for Authentication
def authenticate(token):
    if not token or not token.startswith('Bearer '):
        return None

    id_token = token.split(' ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        claims = decoded_token.get('claims', {})
        return {'uid': user_id, 'admin': claims.get('admin', False)}
    except Exception as e:
        return None
    

@app.route("/setAdminRole", methods=["POST"])
def set_admin_role():
    user = authenticate(request.headers.get('Authorization'))
    if not user or not user.get('admin', False):
        return jsonify({"error": "Unauthorized"}), 401

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
    user = authenticate(request.headers.get('Authorization'))
    if not user or not user.get('admin', False):
        return jsonify({"error": "Unauthorized"}), 401
    
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