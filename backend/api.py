from flask import Flask, request, jsonify
from flask_cors import CORS
from database.db import SessionLocal, init_db
from database.create_superadmin import create_superadmin

from entities.consultant import Consultant
from entities.client import Client
from entities.booking import Booking
from entities.service import Service
from entities.admin import Admin
from entities.timeslot import TimeSlot

from services.booking_service import BookingService
from services.availability_service import AvailabilityService

from ai.ai_service import ask_ai

from datetime import datetime

app = Flask(__name__)
CORS(app)


# -------------------------
# database initialization 
# -------------------------

@app.before_request
def startup():
    init_db()

# -------------------------
# create superadmin
# -------------------------

create_superadmin()

# -------------------------
# Health Check
# -------------------------
@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

# -------------------------
# necessary dependancies 
# -------------------------

db = SessionLocal()
availability_service = AvailabilityService(db)
booking_service = BookingService(db)
system_policy = SystemPolicy(db)
notifier = NotificationService(db)

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

# -------------------------
# load admin
# -------------------------
def load_admins():
    db = SessionLocal()
    try:
        all_admins = db.query(Admin).all()
        admin_dict = {admin.user_id: admin for admin in all_admins}
        return admin_dict
    finally:
        db.close()

# Load admins at startup
admins = load_admins()

# -------------------------
# Consultant login
# -------------------------
@app.route("/api/consultant/login", methods=["POST"])
def consultant_login():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    password = data.get("password")
    consultant = users.get(user_id)

    if not consultant:
        return jsonify({"success": False, "message": "Consultant not found"}), 404

    # Check approval FIRST
    if not consultant.approved:
        return jsonify({
            "success": False,
            "message": "Consultant not approved yet"
        }), 403

    # Then check password
    if consultant.logIn(password):
        return jsonify({
            "success": True,
            "consultant_id": consultant.user_id,
            "name": consultant.name
        })

    return jsonify({
        "success": False,
        "message": "Invalid password"
    }), 401
    
# -------------------------
# Consultant Signup
# -------------------------
@app.route("/api/consultant/signup", methods=["POST"])
def consultant_signup():
    db = SessionLocal()
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

    # Check if already exists
    if user_id in users:
        return jsonify({
            "success": False,
            "message": "User ID already exists"
        }), 400

    # Create new consultant (approved = False by default)
    consultant = Consultant(user_id, name, email, password)
    users[user_id] = consultant

    print(f"New consultant created: {consultant}")

        return jsonify({
            "success": True,
            "message": "Consultant registered successfully. Awaiting approval."
        }), 201
    finally:
        db.close()

# -------------------------
# Get consultant bookings
# -------------------------
@app.route("/api/consultant/<consultant_id>/bookings", methods=["GET"])
def get_bookings(consultant_id):
    db = SessionLocal()
    try:
        consultant = db.query(Consultant).filter_by(user_id=consultant_id).first()
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

        return jsonify(bookings_list), 200
    finally:
        db.close()

# -------------------------
# Confirm Booking
# -------------------------
@app.route("/api/bookings/<booking_id>/confirm", methods=["POST"])
def confirm_booking(booking_id):
    db = SessionLocal()
    try:
        booking = db.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify({"message": "Booking not found"}), 404

        BookingService(db).confirm_booking(booking)
        db.commit()

        return jsonify({"message": "Booking confirmed"}), 200
    finally:
        db.close()

# -------------------------
# Reject Booking
# -------------------------
@app.route("/api/bookings/<booking_id>/reject", methods=["POST"])
def reject_booking(booking_id):
    db = SessionLocal()
    try:
        booking = db.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify({"message": "Booking not found"}), 404

        BookingService(db).reject_booking(booking)
        db.commit()

        return jsonify({"message": "Booking rejected"}), 200
    finally:
        db.close()

# -------------------------
# Get Timeslots
# -------------------------
@app.route("/api/consultant/<consultant_id>/timeslots", methods=["GET"])
def get_timeslots(consultant_id):
    db = SessionLocal()
    try:
        consultant = db.query(Consultant).filter_by(user_id=consultant_id).first()
        if not consultant:
            return jsonify({"message": "Consultant not found"}), 404

        return jsonify([
            {
                "slot_id": ts.slot_id,
                "start_time": ts.start_time.isoformat(),
                "end_time": ts.end_time.isoformat()
            } for ts in consultant.timeslots
        ])
    finally:
        db.close()

# -------------------------
# Add Timeslot
# -------------------------
@app.route("/api/consultant/<consultant_id>/timeslots", methods=["POST"])
def add_timeslot(consultant_id):
    db = SessionLocal()
    try:
        data = request.get_json()

        consultant = db.query(Consultant).filter_by(user_id=consultant_id).first()
        if not consultant:
            return jsonify({"message": "Consultant not found"}), 404

        slot = TimeSlot(
            slot_id=f"ts{datetime.now().timestamp()}",
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"])
        )

        consultant.timeslots.append(slot)
        db.add(slot)
        db.commit()

        return jsonify({"message": "Timeslot added"}), 201
    finally:
        db.close()

# -------------------------
# Delete Timeslot
# -------------------------
@app.route("/api/consultant/<consultant_id>/timeslots/<slot_id>/delete", methods=["POST"])
def delete_timeslot(consultant_id, slot_id):
    db = SessionLocal()
    try:
        slot = db.query(TimeSlot).filter_by(slot_id=slot_id).first()
        if not slot:
            return jsonify({"message": "Timeslot not found"}), 404

        db.delete(slot)
        db.commit()

        return jsonify({"message": "Timeslot deleted"}), 200
    finally:
        db.close()

# -------------------------
# Get Services (Consultant)
# -------------------------
@app.route("/api/consultant/<consultant_id>/services", methods=["GET"])
def get_consultant_services(consultant_id):
    db = SessionLocal()
    try:
        services = db.query(Service).filter_by(consultant_id=consultant_id).all()

        return jsonify([
            {
                "service_id": s.service_id,
                "serviceName": s.serviceName,
                "duration": s.duration,
                "price": s.price
            } for s in services
        ])
    finally:
        db.close()

# -------------------------
# Add Service
# -------------------------
@app.route("/api/consultant/<consultant_id>/services", methods=["POST"])
def add_service(consultant_id):
    db = SessionLocal()
    try:
        data = request.get_json()

        service = Service(
            service_id=f"s{datetime.now().timestamp()}",
            serviceName=data["serviceName"],
            duration=data["duration"],
            price=data["price"],
            consultant_id=consultant_id
        )

        db.add(service)
        db.commit()

        return jsonify({"message": "Service added"}), 201
    finally:
        db.close()

# -------------------------
# Delete Service
# -------------------------
@app.route("/api/consultant/<consultant_id>/services/<service_id>/delete", methods=["POST"])
def delete_service(consultant_id, service_id):
    db = SessionLocal()
    try:
        service = db.query(Service).filter_by(service_id=service_id).first()
        if not service:
            return jsonify({"message": "Service not found"}), 404

        db.delete(service)
        db.commit()

        return jsonify({"message": "Service deleted"}), 200
    finally:
        db.close()

# -------------------------
# Admin Login
# -------------------------
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    db = SessionLocal()
    try:
        data = request.get_json()
        admin = db.query(Admin).filter_by(user_id=data.get("user_id")).first()

        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404

        if admin.logIn(data.get("password")):
            return jsonify({
                "success": True,
                "admin_id": admin.user_id,
                "name": admin.name
            }), 200

        return jsonify({"success": False, "message": "Invalid password"}), 401
    finally:
        db.close()
        
# -------------------------
# get all consultants for admin 
# -------------------------
@app.route("/api/admin/consultants", methods=["GET"])
def get_consultants():
    db = SessionLocal()
    try:
        consultants = db.query(Consultant).all()
        consultants_list = [{
            "user_id": c.user_id,
            "name": c.name,
            "email": c.email,
            "approved": c.approved
        } for c in consultants]
        return jsonify(consultants_list), 200
    finally:
        db.close()
        
# -------------------------
#approve consultant endpoint
# -------------------------

@app.route("/api/admin/approve/<consultant_id>", methods=["POST"])
def approve_consultant(consultant_id):
    db = SessionLocal()
    try:
        data = request.get_json()
        admin = db.query(Admin).filter_by(user_id=data.get("admin_id")).first()
        if not admin:
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        consultant = db.query(Consultant).filter_by(user_id=consultant_id).first()
        if not consultant:
            return jsonify({"success": False, "message": "Consultant not found"}), 404

        consultant.approved = True
        db.commit()

        return jsonify({"success": True, "message": "Consultant approved"}), 200
    finally:
        db.close()
        
# -------------------------
#get policies for admin
# -------------------------

@app.route("/api/admin/get-policies", methods=["GET"])
def get_policies():
    db = SessionLocal()
    try:
        admin_id = request.args.get("admin_id")

        admin = db.query(Admin).filter_by(user_id=admin_id).first()
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404

        return jsonify({
            "cancellationRules": admin.system_policy.cancellationRules,
            "pricingStrategy": admin.system_policy.pricingStrategy,
            "refundPolicy": admin.system_policy.refundPolicy
        }), 200
    finally:
        db.close()

# -------------------------
#admin update policy 
# -------------------------

@app.route("/api/admin/update-policy", methods=["POST"])
def update_policy():
    db = SessionLocal()
    try:
        data = request.get_json()
        admin_id = data.get("admin_id")

        admin = db.query(Admin).filter_by(user_id=admin_id).first()
        if not admin:
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        admin.updatePolicies(
            cancellation_rules=data.get("cancellation_rules"),
            pricing_strategy=data.get("pricing_strategy"),
            refund_policy=data.get("refund_policy")
        )

        db.commit()

        return jsonify({"success": True, "message": "Policies updated"}), 200
    finally:
        db.close()

# -------------------------
# AI Chat
# -------------------------
@app.route("/api/chat", methods=["POST"])
def chat_with_ai():
    data = request.get_json(force=True)
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    reply = ask_ai(user_message)
    return jsonify({"reply": reply}), 200

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)