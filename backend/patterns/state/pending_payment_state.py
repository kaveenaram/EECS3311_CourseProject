from .booking_state import BookingState
from .paid_state import PaidState
from .cancelled_state import CancelledState

class PendingPaymentState(BookingState):
    # once payment is successful, payment_service will call the paid method on the booking
    # (only allowed if it is currently in pending payment state)
    # which will transition the booking to the paid state and mark the timeslot as unavailable
    def paid(self, booking, amount: float):
        # payment received
        self._set_state(PaidState())
        if hasattr(booking, 'timeslot') and booking.timeslot is not None:
            try:
                booking.timeslot.mark_unavailable()
            except Exception:
                pass
        return booking

    def cancel(self, booking):
        booking._set_state(CancelledState())
        return booking