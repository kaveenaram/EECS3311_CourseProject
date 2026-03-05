from entities.booking import Booking
from entities.timeslot import TimeSlot
from entities.client import Client
from entities.consultant import Consultant
from entities.service import Service


class BookingService:

    def __init__(self):
        self.bookings = []

    def create_booking(self, client: Client, consultant: Consultant, service: Service, slot: TimeSlot) -> Booking:

        # Slot availability
        if not slot.available:
            raise Exception("Timeslot is not available.")

        # Ensure slot belongs to consultant
        if slot not in consultant.timeslots:
            raise Exception("Timeslot does not belong to consultant.")

        # Create booking
        booking = Booking(
            client,
            consultant,
            service,
            slot
        )
        self.bookings.append(booking)
        client.bookings.append(booking)
        return booking

  
    def confirm_booking(self, booking):
        booking.confirm()

        # Remove slot after confirm
        booking.timeslot.mark_unavailable()

    

    def reject_booking(self, booking: Booking):
        booking.reject()
    def cancel_booking(self, booking: Booking):
        booking.cancel()
    def complete_booking(self, booking: Booking):
        booking.complete()

    def get_booking(self, booking_id: str) -> Booking:
        for book in self.bookings:
            if book.booking_id == booking_id:
                return book
        raise Exception("Booking does not exist")

