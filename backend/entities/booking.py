from backend.patterns.observer import observer
from typing import List, Any
from backend.patterns.state.booking_state import BookingState
from backend.patterns.state.pending_payment_state import PendingPaymentState
from backend.patterns.state.requested_state import RequestedState
from backend.patterns.observer.subject import Subject

class Booking:

    def __init__(self, booking_id: str, client_id: str, consultant_id: str, service_id: str, slot_id: str, state: str):
      self.booking_id = booking_id
      self.client_id = client_id
      self.consultant_id = consultant_id
      self.service_id = service_id
      self.slot_id = slot_id
      
      self._state: BookingState = RequestedState()

      if hasattr(self._state, "enter"):
        try:
           self._state.enter(self)
        except Exception:
            pass

    # observer helpers are inherited from Subject

    # states called by state objects

    def _set_state(self, new_state) -> None:
        self._state = new_state
        if hasattr(self._state, "enter"):
            try:
                self._state.enter(self)
            except Exception:
                pass
    
    def confirm (self):
       return self._state.confirm(self)
    def reject(self):
       return self._state.reject(self)
    def pending_payment(self):
       return self._state.pending_payment(self)
    def paid(self):
       return self._state.paid(self)
    def cancel(self):
       return self._state.cancel(self)
    def complete(self):
       return self._state.complete(self)
  
    def __str__(self):
      return f"Booking {self.booking_id} | State: {self._state}"
