from .booking_state import BookingState
from .cancelled_state import CancelledState

class ConfirmedState(BookingState):
    # when in confirmed state, booking can be cancelled by the client
    # confirmed means consultant has accepted the booking request, but payment has not been made yet

    def confirm(self, booking):
        # booking is already confirmed, cannot confirm again
        # the booking should be in the pending payment state after being confirmed, so this transition is not allowed
        raise Exception("Booking is already confirmed.")
    
    def cancel(self, booking):
        booking.set_state(CancelledState())
        return booking

