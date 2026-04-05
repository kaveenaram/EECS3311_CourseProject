from sqlalchemy.orm import Session
from entities.service import Service
from entities.timeslot import TimeSlot
from entities.consultant import Consultant

"""
AvailabilityService Class: Manages the availability of services and timeslots for consultants.
Provides methods to add services, manage timeslots, and validate slot availability for bookings.
"""

class AvailabilityService:
    def __init__(self, db: Session):
        self.db = db

    def add_service(self, service: Service):
        self.db.add(service)
        self.db.commit()

    def browse_services(self):
        return self.db.query(Service).all()
    
    def add_timeslot(self, consultant: Consultant, timeslot: TimeSlot):
        timeslot.consultant_id = consultant.consultant_id
        self.db.add(timeslot)
        self.db.commit()

    def remove_timeslot(self, consultant: Consultant, timeslot: TimeSlot):
        timeslot = self.db.query(TimeSlot).filter_by(id=timeslot.slot_id).first()
        if timeslot:
            self.db.delete(timeslot)
            self.db.commit()

    def get_available_slots(self, consultant_id: str):
        return self.db.query(TimeSlot).filter_by(
            consultant_id=consultant_id,
            available=True
        ).all()

    def validate_slot(self, consultant: Consultant, timeslot: TimeSlot) -> bool:
        # Ensures a slot:
        timeslot = self.db.query(TimeSlot).filter_by(
            id=timeslot.slot_id,
            consultant_id=consultant.consultant_id,
            available=True
        ).first()

        if not timeslot:
            raise Exception("Timeslot does not belong to consultant or is unavailable")

        return True

    def mark_slot_unavailable(self, slot_id: str, consultant_id: str):
        timeslot = self.db.query(TimeSlot).filter_by(
            slot_id=slot_id,
            consultant_id=consultant_id
        ).first()
        if timeslot:
            timeslot.mark_unavailable()
            self.db.commit()
