from .booking_state import BookingState
from .cancelled_state import CancelledState
from .completed_state import CompletedState

class PaidState(BookingState):
    def enter(self, booking):
        if hasattr(booking, 'timeslot') and booking.timeslot is not None:
            try:
                booking.timeslot.mark_unavailable()
            except Exception:
                pass
        return booking
    
    def complete(self, booking):
        # payment was made, booking took place
        # booking is completed
        booking._set_state(CompletedState())
        return booking
    
    def cancel(self, booking):
        # booking can be cancelled
        # admin refund polices take place
        # !!!!!!! await admin_service completion !!!!!!!

        booking._set_state(CancelledState())
        return booking
