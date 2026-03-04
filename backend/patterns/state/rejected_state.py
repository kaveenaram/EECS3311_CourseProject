from .booking_state import BookingState

class RejectedState(BookingState):
    def enter(self, booking):
        booking.notifyObservers("Booking has been rejected.")
        return booking
    
    def __str__(self):
        return "This booking has been rejected."
