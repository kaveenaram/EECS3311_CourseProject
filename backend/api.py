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
from entities.payment_result import PaymentResult

from services.booking_service import BookingService
from services.availability_service import AvailabilityService

from ai.ai_service import ask_ai

from datetime import datetime

app = Flask(__name__)
CORS(app)


# -------------------------
# database initialization 
# -------------------------

admin_created = False

@app.before_request
def startup():
    global admin_created
    init_db()
    if not admin_created:
        create_superadmin()
        admin_created = True

# -------------------------
# Health Check
# -------------------------
@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

# -------------------------
# Home
# -------------------------
@app.route("/")
def home():
    return "API is running"

# -------------------------
# Get all services
# -------------------------
@app.route('/api/services', methods=['GET'])
def get_services():
    db = SessionLocal()
    try:
        services = db.query(Service).all()
        return [
            {
                'service_id': s.service_id,
                'serviceName': s.name,
                'name': s.name,
                'description': s.description,
                'duration': s.duration,
                'price': s.price,
                'consultant_id': s.consultant_id
            }
            for s in services
        ], 200
    except Exception as e:
        print(f"Error fetching services: {e}")
        return {'error': str(e)}, 500
    finally:
        db.close()

# -------------------------
# Consultant login
# -------------------------
@app.route("/api/consultant/login", methods=["POST"])
def consultant_login():
    db = SessionLocal()
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        password = data.get("password")

        consultant = db.query(Consultant).filter_by(user_id=user_id).first()

        if not consultant:
            return jsonify({"success": False, "message": "Consultant not found"}), 404

        if not consultant.approved:
            return jsonify({
                "success": False,
                "message": "Consultant not approved yet"
            }), 403

        if consultant.logIn(password):
            return jsonify({
                "success": True,
                "consultant_id": consultant.user_id,
                "name": consultant.name
            }), 200

        return jsonify({"success": False, "message": "Invalid password"}), 401
    finally:
        db.close()

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

        existing = db.query(Consultant).filter_by(user_id=user_id).first()
        if existing:
            return jsonify({
                "success": False,
                "message": "User ID already exists"
            }), 400

        consultant = Consultant(user_id, name, email, password)
        db.add(consultant)
        db.commit()

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
# Create Booking (Client)
# -------------------------
# Create Booking (Client)
# -------------------------
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    db = SessionLocal()
    try:
        data = request.get_json()
        client_id = data.get("client_id")
        consultant_id = data.get("consultant_id")
        service_id = data.get("service_id")
        slot_id = data.get("slot_id")
        
        # Validate all required fields
        if not all([client_id, consultant_id, service_id, slot_id]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        # Get client
        client = db.query(Client).filter_by(user_id=client_id).first()
        if not client:
            return jsonify({"success": False, "message": "Client not found"}), 404
        
        # Get consultant
        consultant = db.query(Consultant).filter_by(user_id=consultant_id).first()
        if not consultant:
            return jsonify({"success": False, "message": "Consultant not found"}), 404
        
        # Get service
        service = db.query(Service).filter_by(service_id=service_id).first()
        if not service:
            return jsonify({"success": False, "message": "Service not found"}), 404
        
        # Get timeslot
        timeslot = db.query(TimeSlot).filter_by(slot_id=slot_id).first()
        if not timeslot:
            return jsonify({"success": False, "message": "Timeslot not found"}), 404
        
        if not timeslot.available:
            return jsonify({"success": False, "message": "Timeslot is no longer available"}), 409
        
        # Create booking using BookingService
        booking_service = BookingService(db)
        booking = booking_service.create_booking(client, consultant, service, timeslot)
        
        return jsonify({
            "success": True,
            "message": "Booking created successfully",
            "booking_id": booking.booking_id,
            "state": str(booking.state)
        }), 201
    except Exception as e:
        print(f"Error creating booking: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/consultant/<consultant_id>/available-slots", methods=["GET"])
def get_available_slots(consultant_id):
    """Get available slots split by service duration if applicable"""
    db = SessionLocal()
    try:
        service_id = request.args.get("service_id")
        
        if not service_id:
            return jsonify({"error": "service_id parameter required"}), 400
        
        # Get the service to determine duration
        service = db.query(Service).filter_by(service_id=service_id).first()
        if not service:
            return jsonify({"error": "Service not found"}), 404
        
        service_duration = service.duration  # in minutes
        
        # Get all available timeslots for consultant
        timeslots = db.query(TimeSlot).filter_by(
            consultant_id=consultant_id,
            available=True
        ).all()
        
        available_slots = []
        
        for slot in timeslots:
            # Calculate slot duration in minutes
            slot_duration = (slot.end_time - slot.start_time).total_seconds() / 60
            
            # If slot is larger than service duration, split it
            if slot_duration > service_duration:
                # Create multiple booking options
                current_time = slot.start_time
                while (slot.end_time - current_time).total_seconds() / 60 >= service_duration:
                    end_time = current_time + __import__('datetime').timedelta(minutes=service_duration)
                    available_slots.append({
                        'slot_id': slot.slot_id,
                        'start_time': current_time.isoformat(),
                        'end_time': end_time.isoformat(),
                        'available': True,
                        'original_slot_id': slot.slot_id
                    })
                    current_time = end_time
            else:
                # Slot is exact size or smaller
                available_slots.append({
                    'slot_id': slot.slot_id,
                    'start_time': slot.start_time.isoformat(),
                    'end_time': slot.end_time.isoformat(),
                    'available': True,
                    'original_slot_id': slot.slot_id
                })
        
        return jsonify(available_slots), 200
    except Exception as e:
        print(f"Error fetching available slots: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# -------------------------
# Get Timeslots
# -------------------------
@app.route("/api/consultant/<consultant_id>/timeslots", methods=["GET"])
def get_timeslots(consultant_id):
    db = SessionLocal()
    try:
        timeslots = db.query(TimeSlot).filter_by(consultant_id=consultant_id).all()
        
        return jsonify([
            {
                "slot_id": ts.slot_id,
                "start_time": ts.start_time.isoformat(),
                "end_time": ts.end_time.isoformat(),
                "available": ts.available if hasattr(ts, 'available') else True
            } for ts in timeslots
        ])
    except Exception as e:
        print(f"Error fetching timeslots: {e}")
        return jsonify({"error": str(e)}), 500
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

        # Parse time strings (format: "HH:MM" from HTML time input) and date (format: "YYYY-MM-DD")
        from datetime import time as dt_time
        try:
            start_time_str = data.get("start_time")
            end_time_str = data.get("end_time")
            date_str = data.get("date")  # Optional date in YYYY-MM-DD format
            
            # Parse times
            start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time_str, "%H:%M").time()
            
            # Use provided date or default to today
            if date_str:
                try:
                    slot_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    slot_date = datetime.now().date()
            else:
                slot_date = datetime.now().date()
            
            start_datetime = datetime.combine(slot_date, start_time_obj)
            end_datetime = datetime.combine(slot_date, end_time_obj)
            
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing time: {e}")
            return jsonify({"error": f"Invalid time format: {e}"}), 400

        slot = TimeSlot(
            slot_id=f"ts{datetime.now().timestamp()}",
            start_time=start_datetime,
            end_time=end_datetime,
            consultant_id=consultant_id
        )

        db.add(slot)
        db.commit()

        return jsonify({
            "slot_id": slot.slot_id,
            "start_time": slot.start_time.isoformat(),
            "end_time": slot.end_time.isoformat(),
            "available": True
        }), 201
    except Exception as e:
        print(f"Error adding timeslot: {e}")
        return jsonify({"error": str(e)}), 500
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
                "name": s.name,
                "serviceName": s.name,
                "duration": s.duration,
                "price": s.price
            } for s in services
        ])
    except Exception as e:
        print(f"Error fetching consultant services: {e}")
        return jsonify({"error": str(e)}), 500
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

        consultant = db.query(Consultant).filter_by(user_id=consultant_id).first()
        if not consultant:
            return jsonify({"message": "Consultant not found"}), 404

        service = Service(
            service_id=f"s{datetime.now().timestamp()}",
            serviceName=data["serviceName"],
            duration=data["duration"],
            price=data["price"],
            consultant=consultant
        )

        db.add(service)
        db.commit()

        return jsonify({
            "service_id": service.service_id,
            "serviceName": service.name,
            "duration": service.duration,
            "price": service.price,
            "consultant_id": service.consultant_id
        }), 201
    except Exception as e:
        print(f"Error adding service: {e}")
        return jsonify({"error": str(e)}), 500
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
# Client login
# -------------------------
@app.route("/api/client/login", methods=["POST"])
def client_login():
    db = SessionLocal()
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        password = data.get("password")

        client = db.query(Client).filter_by(user_id=user_id).first()

        if not client:
            return jsonify({"success": False, "message": "Client not found"}), 404

        if client.logIn(password):
            return jsonify({
                "success": True,
                "client_id": client.user_id,
                "name": client.name
            }), 200

        return jsonify({"success": False, "message": "Invalid password"}), 401
    finally:
        db.close()

# -------------------------
# Client Signup
# -------------------------
@app.route("/api/client/signup", methods=["POST"])
def client_signup():
    db = SessionLocal()
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        existing = db.query(Client).filter_by(user_id=user_id).first()
        if existing:
            return jsonify({
                "success": False,
                "message": "User ID already exists"
            }), 400

        client = Client(user_id, name, email, password)
        db.add(client)
        db.commit()

        return jsonify({
                "success": True,
                "message": "Client registered successfully."
            }), 201
    finally:
        db.close()

# -------------------------
# Client Bookings
# -------------------------
@app.route("/api/client/<client_id>/bookings", methods=["GET"])
def get_client_bookings(client_id):
    db = SessionLocal()
    try:
        client = db.query(Client).filter_by(user_id=client_id).first()
        if not client:
            return jsonify({"success": False, "message": "Client not found"}), 404

        bookings_list = []
        for booking in client.bookings:
            bookings_list.append({
                'booking_id': booking.booking_id,
                'service_id': booking.service_id,
                'consultant_id': booking.consultant_id,
                'state': str(booking.get_state()),
                'created_at': booking.created_at.isoformat() if booking.created_at else None,
                'timeslot_id': booking.timeslot_id
            })
        
        return jsonify(bookings_list), 200
    except Exception as e:
        print(f"Error fetching client bookings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# -------------------------
# Client Payments
# -------------------------
@app.route("/api/client/<client_id>/payments", methods=["GET"])
def get_client_payments(client_id):
    db = SessionLocal()
    try:
        client = db.query(Client).filter_by(user_id=client_id).first()
        if not client:
            return jsonify({"success": False, "message": "Client not found"}), 404

        payments_list = []
        
        # Get all bookings for this client
        for booking in client.bookings:
            # Get payment history for this booking
            if booking.payment_history:
                for payment in booking.payment_history:
                    payments_list.append({
                        'payment_id': payment.user_id,
                        'booking_id': payment.booking_id,
                        'amount': payment.amount,
                        'status': 'COMPLETED' if payment.success else 'FAILED',
                        'created_at': payment.timestamp.isoformat() if payment.timestamp else None
                    })
        
        return jsonify(payments_list), 200
    except Exception as e:
        print(f"Error fetching client payments: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# -------------------------
# Cancel Booking
# -------------------------
@app.route("/api/bookings/<booking_id>/cancel", methods=["POST"])
def cancel_booking(booking_id):
    db = SessionLocal()
    try:
        booking = db.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify({"success": False, "message": "Booking not found"}), 404
        
        # Get current state and try to cancel
        current_state = booking.get_state()
        
        # You can only cancel if not already cancelled or completed
        if str(current_state) == "CANCELLED" or str(current_state) == "COMPLETED":
            return jsonify({
                "success": False,
                "message": f"Cannot cancel a booking in {current_state} state"
            }), 400
        
        # Request cancellation (this will trigger state transition)
        booking.request_cancellation()
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "Booking cancelled successfully"
        }), 200
    except Exception as e:
        print(f"Error cancelling booking: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        db.close()

# -------------------------
# Admin - All Payments
# -------------------------
@app.route("/api/admin/all-payments", methods=["GET"])
def get_all_payments():
    db = SessionLocal()
    try:
        admin_id = request.args.get("admin_id")
        
        # Verify admin exists
        admin = db.query(Admin).filter_by(user_id=admin_id).first()
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
        
        # Get all payment results
        all_payments = db.query(PaymentResult).all()
        
        payments_list = []
        for payment in all_payments:
            payments_list.append({
                'payment_id': payment.user_id if payment.user_id else str(payment.timestamp),
                'booking_id': payment.booking_id,
                'amount': float(payment.amount) if payment.amount else 0,
                'status': 'COMPLETED' if payment.success else 'FAILED',
                'timestamp': payment.timestamp.isoformat() if payment.timestamp else None
            })
        
        return jsonify(payments_list), 200
    except Exception as e:
        print(f"Error fetching all payments: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# -------------------------
# Admin - All Bookings
# -------------------------
@app.route("/api/admin/all-bookings", methods=["GET"])
def get_all_bookings():
    db = SessionLocal()
    try:
        admin_id = request.args.get("admin_id")
        
        # Verify admin exists
        admin = db.query(Admin).filter_by(user_id=admin_id).first()
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
        
        # Get all bookings
        all_bookings = db.query(Booking).all()
        
        bookings_list = []
        for booking in all_bookings:
            bookings_list.append({
                'booking_id': booking.booking_id,
                'client_id': booking.client_id,
                'consultant_id': booking.consultant_id,
                'service_id': booking.service_id,
                'timeslot_id': booking.timeslot_id,
                'state': str(booking.get_state()),
                'created_at': booking.created_at.isoformat() if booking.created_at else None
            })
        
        return jsonify(bookings_list), 200
    except Exception as e:
        print(f"Error fetching all bookings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)