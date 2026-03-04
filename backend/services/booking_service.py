from models.booking import Booking
from models.timeslot import TimeSlot


class BookingService:

    def create_booking(self, booking_id, client, consultant, service, slot: TimeSlot):

        # Slot availability
        if not slot.available:
            raise Exception("Selected timeslot is not available.")

        # Ensure slot belongs to consultant
        if slot not in consultant.timeslots:
            raise Exception("Timeslot does not belong to consultant.")

        # Create booking
        booking = Booking(
            booking_id,
            client,
            consultant,
            service,
            slot
        )
        return booking

  
    def confirm_booking(self, booking):
        booking.confirm()

        # Remove slot after confirm
        booking.timeslot.mark_unavailable()
