from flask import Flask, jsonify
from flask_cors import CORS
from database.db import SessionLocal, init_db
from services.booking_service import BookingService
from services.availability_service import AvailabilityService
from services.payment_service import PaymentService

app = Flask(__name__)
CORS(app)

@app.before_request
def startup():
    init_db()

@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

@app.route('/api/services', methods=['GET'])
def get_services():
    db = SessionLocal()
    try:
        service = AvailabilityService(db)
        services = service.browse_services()
    finally:
        db.close()
    return {'services': [s.name for s in services]}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)