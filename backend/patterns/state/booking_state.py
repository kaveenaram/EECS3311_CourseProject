from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.booking import Booking

from abc import ABC
from typing import Any

"""
BookingState Class: Abstract base class representing the state of a booking in the system.
Concrete implementations will define specific behaviors for each booking state.
"""

class BookingState(ABC):
    # initial state when a client submits a booking request is the requested state
    # interface for booking states
    # concrete states will override allowed transitions
    def confirm(self, booking: "Booking"):
        raise Exception("Invalid state transition: Booking cannot be confirmed from the current state")
    def reject(self, booking: "Booking"):
        raise Exception("Invalid state transition: Booking cannot be rejected from the current state")
    def pending_payment(self, booking: "Booking"):
        raise Exception("Invalid state transition: Booking cannot be marked as pending payment from the current state")
    def paid(self, booking: "Booking", amount: float):
        raise Exception("Invalid state transition: Booking cannot be marked as paid from the current state")
    def cancel(self, booking: "Booking"):
        raise Exception("Invalid state transition: Booking cannot be cancelled from the current state")
    def complete(self, booking: "Booking"):
        raise Exception("Invalid state transition: Booking cannot be marked as completed from the current state")

