from entities.booking import Booking
from entities.timeslot import TimeSlot
from entities.client import Client
from entities.consultant import Consultant
from entities.service import Service

"""
BookingService Class: Handles the core logic for managing bookings, including creating, confirming, rejecting, cancelling, and completing bookings.
Provides methods to create a booking by validating slot availability and associating it with the client and consultant, as well as methods to update the booking status and retrieve bookings by ID.
"""

# UPDATED IN PHASE 2
    # BookingService now interacts with the database

from sqlalchemy.orm import Session
import uuid

class BookingService:

    def __init__(self, db: Session):
        self.db = db

    def create_booking(self, client: Client, consultant: Consultant, service: Service, slot: TimeSlot) -> Booking:

        # Slot availability
        # db query
        db_slot = self.db.query(TimeSlot).filter_by(
            slot_id=slot.slot_id,
            available=True
        ).first()

        if not db_slot:
            raise Exception("Timeslot is not available.")

        # Ensure slot belongs to consultant
        if db_slot.consultant_id != consultant.id:
            raise Exception("Timeslot does not belong to consultant.")

        # Create booking
        booking = Booking(client, consultant, service, slot)

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        
        return booking

  
    def confirm_booking(self, booking):
        booking.confirm()

        # Remove slot after confirm
        db_slot = self.db.query(TimeSlot).filter_by(
            slot_id=booking.timeslot_id
        ).first()
        db_slot.mark_unavailable()
        self.db.commit()

    

    def reject_booking(self, booking: Booking):
        booking.reject()
        self.db.commit()
    def cancel_booking(self, booking: Booking):
        booking.cancel()
        db_slot = self.db.query(TimeSlot).filter_by(id=booking.timeslot_id).first()
        if db_slot:
            db_slot.mark_available()
        self.db.commit()

    def complete_booking(self, booking: Booking):
        booking.complete()
        self.db.commit()

    def get_booking(self, booking_id: str) -> Booking:
        booking = self.db.query(Booking).filter_by(booking_id=booking_id).first()
        if not booking:
            raise Exception("Booking does not exist")
        return booking

