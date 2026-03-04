from .booking_state import BookingState
from .confirmed_state import ConfirmedState
from .pending_payment_state import PendingPaymentState
from .rejected_state import RejectedState
from .cancelled_state import CancelledState

class RequestedState(BookingState):
    # when in the requested state
    # booking can be confirmed by the consultant, then can be set to a pending payment state
    # booking can be rejected by the consultant
    # booking can be cancelled by the client

    def confirm(self, booking):
        booking._set_state(ConfirmedState())
        booking.notifyObservers("Booking has been confirmed.")
        booking._set_state(PendingPaymentState())
        return booking
    
    def reject(self, booking):
        booking._set_state(RejectedState())
        booking.notifyObservers("Booking has been rejected.")
        return booking
    
    def cancel(self, booking):
        booking._set_state(CancelledState())
        return booking