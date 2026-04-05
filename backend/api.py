from flask import Flask, request, jsonify
from services.booking_service import BookingService
from services.availability_service import AvailabilityService
from services.payment_service import PaymentService
from entities.client import Client
from entities.consultant import Consultant
from entities.admin import Admin
from entities.system_policy import SystemPolicy
from patterns.observer.notification_service import NotificationService

app = Flask(__name__)

# -------------------------------
# TEMP USERS (until database is connected)
# -------------------------------
notifier = NotificationService()
system_policy = SystemPolicy()

users = {
    "client1": Client("client1", "Client One", "client@domain.com", "password"),
    "consultant1": Consultant("consultant1", "Consultant One", "consultant@domain.com", "password"),
    "admin1": Admin("admin1", "Admin One", "admin@domain.com", "password", system_policy, notifier)
}

availability_service = AvailabilityService()
booking_service = BookingService()
payment_service = PaymentService()

# -------------------------------
# TEST ROUTE
# -------------------------------
@app.route("/")
def home():
    return "API is running"

# -------------------------------
# GET ALL BOOKINGS (Admin view or all consultants)
# -------------------------------
@app.route("/booking-requests", methods=["GET"])
def get_booking_requests():
    all_bookings = []

    # loop through all consultants to gather bookings
    for user in users.values():
        if isinstance(user, Consultant):
            all_bookings.extend(user.get_bookings())

    result = []
    for b in all_bookings:
        result.append({
            "id": b.booking_id,
            "client": b.client.name,
            "service": b.service.serviceName,
            "status": str(b.get_state()),
            "consultant": b.consultant.name
        })

    return jsonify(result)
# -------------------------------
# Get consultant bookings
# -------------------------------

@app.route("/consultant/<consultant_id>/bookings", methods=["GET"])
def get_consultant_bookings(consultant_id):
    consultant = users.get(consultant_id)
    if not consultant or not isinstance(consultant, Consultant):
        return jsonify({"error": "Consultant not found"}), 404

    bookings = consultant.get_bookings()
    result = []
    for b in bookings:
        result.append({
            "id": b.booking_id,
            "client": b.client.name,
            "service": b.service.serviceName,
            "status": str(b.get_state()),
            "timeslot": f"{b.timeslot.start_time} - {b.timeslot.end_time}"
        })

    return jsonify(result)

# -------------------------------
# ACCEPT BOOKING
# -------------------------------
@app.route("/booking-requests/<booking_id>/accept", methods=["POST"])
def accept_booking(booking_id):
    try:
        booking = booking_service.get_booking(booking_id)
        booking_service.confirm_booking(booking)
        return jsonify({"message": "Booking accepted"})
    except Exception:
        return jsonify({"error": "Booking not found"}), 404

# -------------------------------
# REJECT BOOKING
# -------------------------------
@app.route("/booking-requests/<booking_id>/reject", methods=["POST"])
def reject_booking(booking_id):
    try:
        booking = booking_service.get_booking(booking_id)
        booking_service.reject_booking(booking)
        return jsonify({"message": "Booking rejected"})
    except Exception:
        return jsonify({"error": "Booking not found"}), 404

# -------------------------------
# GET USERS (Admin Dashboard)
# -------------------------------
@app.route("/users", methods=["GET"])
def get_users():
    result = []
    for user in users.values():
        result.append({
            "id": user.user_id,
            "name": user.name,
            "role": type(user).__name__  # Admin, Consultant, or Client
        })
    return jsonify(result)

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)