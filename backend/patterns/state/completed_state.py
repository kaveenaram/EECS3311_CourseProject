from .booking_state import BookingState

class CompletedState(BookingState):
    def __str__(self):
        return "This booking has been completed."