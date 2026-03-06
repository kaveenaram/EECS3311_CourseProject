from typing import TYPE_CHECKING, List, Any

import uuid 
from patterns.observer import observer
from patterns.state.pending_payment_state import PendingPaymentState
from patterns.state.requested_state import RequestedState
from patterns.observer.subject import Subject

if TYPE_CHECKING:
   from patterns.state.booking_state import BookingState  # only for type hints

"""
Booking Class: Represents a booking made by a client for a consulting session with a consultant, including details like client, consultant, service, timeslot, and booking state.
Implements the Subject interface for the Observer pattern to notify observers (like clients and consultants) of state changes, and uses the State pattern to manage booking states and transitions.
"""

class Booking(Subject):

   # Booking constructor initializes booking attributes including client, consultant, service, timeslot, and sets the initial state to RequestedState. It also initializes an empty list of observers for the Observer pattern.
   def __init__(self, client, consultant, service, timeslot, state: str = None):
      self.booking_id = str(uuid.uuid4()) #auto generate booking id 
      self.client = client
      self.consultant = consultant
      self.service = service
      self.timeslot = timeslot
      
      self._observers: List[Any] = []
      self._state: "BookingState" = RequestedState()

      if hasattr(self._state, "enter"):
         try:
            self._state.enter(self)
         except Exception:
            pass

   # Observer pattern methods to attach observers and notify them of state changes.
   # Observers have an update() method that will be called with a message when the booking state changes.
        
   def attachObserver(self, observer):
      self._observers.append(observer)

   def notifyObservers(self, message):
      for observer in self._observers:
         observer.update(message)  # assumes observer has an update() method
      print(message)  # optional: also print to console

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
   def paid(self, amount: float):
      return self._state.paid(self, amount)
   def cancel(self):
      return self._state.cancel(self)
   def complete(self):
      return self._state.complete(self)
  
   def __str__(self):
      return f"Booking {self.booking_id} | State: {self._state}"
