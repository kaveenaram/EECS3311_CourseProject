from .booking_state import BookingState

class CancelledState(BookingState):
    def enter(self, booking):
        booking.notifyObservers("Booking has been cancelled.")
        return booking
    
    def __str__(self):
        return "This booking has been cancelled."