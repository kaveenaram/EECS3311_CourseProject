from .booking_state import BookingState

class RejectedState(BookingState):
    def __str__(self):
        return "This booking has been rejected."
