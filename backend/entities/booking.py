from typing import List, Any
import uuid 
from sqlalchemy import Column, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.patterns.state.requested_state import RequestedState
from database.db import Base
from patterns.observer.subject import Subject
import enum

"""
Booking Class: Represents a booking made by a client for a consulting session with a consultant, including details like client, consultant, service, timeslot, and booking state.
Implements the Subject interface for the Observer pattern to notify observers (like clients and consultants) of state changes, and uses the State pattern to manage booking states and transitions.
"""

class BookingState(enum.Enum):
    requested = "requested"
    confirmed = "confirmed"
    rejected = "rejected"
    pending_payment = "pending_payment"
    paid = "paid"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base, Subject):
    __tablename__ = "bookings"

    booking_id = Column(String, primary_key=True)
    client_id = Column(String, ForeignKey('clients.user_id'))
    consultant_id = Column(String, ForeignKey('consultants.user_id'))
    service_id = Column(String, ForeignKey('services.service_id'))
    timeslot_id = Column(String, ForeignKey('timeslots.slot_id'))
    state = Column(Enum(BookingState), default=BookingState.requested)
    

    payment_history = relationship("PaymentResult", back_populates="booking")
    client = relationship("Client", back_populates="bookings", foreign_keys=[client_id])
    consultant = relationship("Consultant", back_populates="bookings", foreign_keys=[consultant_id])
    service = relationship("Service", back_populates="bookings")
    timeslot = relationship("TimeSlot", back_populates="bookings")

   # Booking constructor initializes booking attributes including client, consultant, service, timeslot, and sets the initial state to RequestedState. It also initializes an empty list of observers for the Observer pattern.
    def __init__(self, client, consultant, service, timeslot):
      self.booking_id = str(uuid.uuid4()) #auto generate booking id 
      self.client = client
      self.consultant = consultant
      self.service = service
      self.timeslot = timeslot
      
      self._observers: List[Any] = []  # List to hold observers for the Observer pattern
      self.state: BookingState.requested # persists to db
      self._state = RequestedState() # stores the state pattern object


   # Observer pattern methods to attach observers and notify them of state changes.
   # Observers have an update() method that will be called with a message when the booking state changes.
        
    def attachObserver(self, observer):
      self._observers.append(observer)

    def notifyObservers(self, message):
      for observer in self._observers:
         observer.update(message)  # assumes observer has an update() method
      print(message)  # optional: also print to console

   # states called by state objects

    def set_state(self, new_state) -> None:
      self._state = new_state
      self.state = new_state.get_state()  # update the state column in the database
      if hasattr(self._state, "enter"):
         try:
            self._state.enter(self)
         except Exception:
            pass
   
    def get_state(self):
      return self.state
   
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
