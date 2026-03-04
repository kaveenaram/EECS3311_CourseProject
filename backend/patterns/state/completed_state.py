from .booking_state import BookingState

class CompletedState(BookingState):
    def enter(self, booking):
        booking.notifyObservers("Booking has been completed.")
        return booking

    def __str__(self):
        return "This booking has been completed."