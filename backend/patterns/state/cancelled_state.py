from .booking_state import BookingState

class CancelledState(BookingState):
    def __str__(self):
        return "This booking has been cancelled."