from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase Admin
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

CORS(app) # Enable CORS for all routes



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
    

@app.route('/events', methods=['GET'])
def get_events():
    events_ref = db.collection('events')
    docs = events_ref.stream()
    events = [{**doc.to_dict(), 'id': doc.id} for doc in docs]
    return jsonify(events)

@app.route('/purchase', methods=['POST'])
def purchase_ticket():
    data = request.json
    user = authenticate(request.headers.get('Authorization'))
    if not user:
        return jsonify({"message": "Unauthorized access."}), 403

    user_id = user['uid']
    event_id = data.get('event_id')
    tickets_to_buy = int(data.get('tickets', 1))  # Default to 1 if not provided

    # Validate the number of tickets to buy
    if tickets_to_buy < 1:
        return jsonify({"message": "Invalid ticket quantity."}), 400

    event_ref = db.collection('events').document(event_id)
    event_snapshot = event_ref.get()

    if not event_snapshot.exists:
        return jsonify({"message": "Event not found."}), 404

    event = event_snapshot.to_dict()

    # Ensure enough tickets are available
    if event['ticketsRemaining'] < tickets_to_buy:
        return jsonify({"message": "Not enough tickets available."}), 400

    try:
        # Use a Firestore transaction to ensure atomic updates
        @firestore.transactional
        def update_tickets(transaction):
            snapshot = event_ref.get(transaction=transaction)
            ticketsRemaining = snapshot.get('ticketsRemaining')

            # Check availability again inside the transaction
            if ticketsRemaining >= tickets_to_buy:
                transaction.update(event_ref, {
                    'ticketsRemaining': ticketsRemaining - tickets_to_buy
                })

                # Create ticket entries in Firestore
                for _ in range(tickets_to_buy):
                    db.collection('tickets').add({
                        'event_id': event_id,
                        'user_id': user_id,
                        'timestamp': firestore.SERVER_TIMESTAMP
                    })
                return True
            return False

        transaction = db.transaction()
        success = update_tickets(transaction)

        if success:
            return jsonify({"message": f"Successfully purchased {tickets_to_buy} tickets!"})
        else:
            return jsonify({"message": "No tickets available."}), 400

    except Exception as e:
        print(f"Error during transaction: {e}")
        return jsonify({"message": "Failed to process the ticket purchase."}), 500

@app.route('/events', methods=['POST'])
def create_event():
    user = authenticate(request.headers.get('Authorization'))
    if not user or not user.get('admin', False):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    required_fields = ['name', 'date', 'location', 'total_tickets']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    try:
        event_data = {
            'name': data['name'],
            'date': data['date'],
            'location': data['location'],
            'totalTickets': data['total_tickets'],
            'ticketsRemaining': data['total_tickets'],
            'created_by': user['uid']
        }
        db.collection('events').add(event_data)
        return jsonify({"message": "Event created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    user = authenticate(request.headers.get('Authorization'))
    if not user or not user.get('admin', False):
        return jsonify({"message": "Unauthorized access."}), 403

    event_ref = db.collection('events').document(event_id)
    event_ref.delete()
    return jsonify({"message": "Event deleted successfully!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
