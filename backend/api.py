from flask import Flask, request, jsonify
from flask_cors import CORS
from entities.consultant import Consultant
from entities.client import Client
from entities.booking import Booking
from services.booking_service import BookingService
from services.availability_service import AvailabilityService

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from React frontend

# Sample in-memory "database", until the database is connected 
users = {
    "consultant1": Consultant("consultant1", "Alice", "alice@mail.com", "pass")
}

clients = {
    "client1": Client("client1", "Bob", "bob@mail.com", "pass")
}

availability_service = AvailabilityService()
booking_service = BookingService()

# For demo: approve the consultant
users["consultant1"].approved = True

#first api check 
@app.route("/")
def home():
    return "API is running"


# -------------------------------
# Consultant login endpoint
# -------------------------------
@app.route("/api/consultant/login", methods=["POST"])
def consultant_login():
    data = request.get_json(force=True)  # force=True ensures JSON parsing
    user_id = data.get("user_id")
    password = data.get("password")

    consultant = users.get(user_id)
    if not consultant:
        return jsonify({"success": False, "message": "Consultant not found"}), 404
    if consultant.logIn(password):
        return jsonify({"success": True, "consultant_id": consultant.user_id, "name": consultant.name})
    else:
        return jsonify({"success": False, "message": "Invalid password"}), 401

# -------------------------------
# Get all bookings for a consultant
# -------------------------------
@app.route("/api/consultant/<consultant_id>/bookings", methods=["GET"])
def get_bookings(consultant_id):
    consultant = users.get(consultant_id)
    if not consultant:
        return jsonify({"success": False, "message": "Consultant not found"}), 404

    bookings_list = []
    for booking in consultant.bookings:
        bookings_list.append({
            "booking_id": booking.booking_id,
            "client_name": booking.client.name,
            "service_name": booking.service.serviceName,
            "start_time": booking.timeslot.start_time,
            "end_time": booking.timeslot.end_time,
            "state": str(booking.get_state())
        })
    return jsonify(bookings_list)

# -------------------------------
# Approve / Reject / Complete booking
# -------------------------------
@app.route("/api/consultant/<consultant_id>/booking/<booking_id>/<action>", methods=["POST"])
def update_booking(consultant_id, booking_id, action):
    consultant = users.get(consultant_id)
    if not consultant:
        return jsonify({"success": False, "message": "Consultant not found"}), 404

    try:
        booking = booking_service.get_booking(booking_id)
        if booking.consultant.user_id != consultant_id:
            return jsonify({"success": False, "message": "Booking does not belong to this consultant"}), 403

        if action == "approve":
            booking_service.confirm_booking(booking)
        elif action == "reject":
            booking_service.reject_booking(booking)
        elif action == "complete":
            booking_service.complete_booking(booking)
        else:
            return jsonify({"success": False, "message": "Invalid action"}), 400

        return jsonify({"success": True, "booking_id": booking.booking_id, "state": str(booking.get_state())})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    

# -------------------------------
# Run Flask server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
