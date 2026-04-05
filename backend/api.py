from flask import Flask, request, jsonify
from flask_cors import CORS
from entities.consultant import Consultant
from entities.client import Client
from entities.booking import Booking
from entities.service import Service
from services.booking_service import BookingService
from services.availability_service import AvailabilityService
from entities.timeslot import TimeSlot
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# -------------------------
# In-memory "database"
# -------------------------
users = {
    "consultant1": Consultant("consultant1", "Alice", "alice@mail.com", "pass")
}

clients = {
    "client1": Client("client1", "Bob", "bob@mail.com", "pass"),
    "client2": Client("client2", "Charlie", "charlie@mail.com", "pass")
}

# Sample services
services = {
    "service1": Service("service1", "Consulting Session", duration=60, price=100, consultant=users["consultant1"]),
    "service2": Service("service2", "Strategy Meeting", duration=90, price=150, consultant=users["consultant1"])
}

availability_service = AvailabilityService()
booking_service = BookingService()

consultant = users["consultant1"]

# -------------------------
# Add timeslots for the consultant
# -------------------------
ts1 = TimeSlot("ts1", datetime.now(), datetime.now() + timedelta(hours=1))
ts2 = TimeSlot("ts2", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=1, hours=1))

consultant.timeslots.extend([ts1, ts2])

# -------------------------
# Create bookings via BookingService
# -------------------------
booking1 = booking_service.create_booking(
    client=clients["client1"],
    consultant=consultant,
    service=services["service1"],
    slot=ts1
)

booking2 = booking_service.create_booking(
    client=clients["client2"],
    consultant=consultant,
    service=services["service2"],
    slot=ts2
)

# -------------------------
# Verify consultant bookings
# -------------------------
print("Consultant bookings:", [b.booking_id for b in consultant.bookings])

# Approve consultant for demo
users["consultant1"].approved = True

# -------------------------
# First API check
# -------------------------
@app.route("/")
def home():
    return "API is running"

@app.route("/api/consultant/login", methods=["POST"])
def consultant_login():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    password = data.get("password")
    consultant = users.get(user_id)

    if not consultant:
        return jsonify({"success": False, "message": "Consultant not found"}), 404
    if consultant.logIn(password):
        return jsonify({"success": True, "consultant_id": consultant.user_id, "name": consultant.name})
    else:
        return jsonify({"success": False, "message": "Invalid password"}), 401

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
            "start_time": booking.timeslot.start_time.isoformat(),
            "end_time": booking.timeslot.end_time.isoformat(),
            "state": str(booking.get_state())
        })
    return jsonify(bookings_list)

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)