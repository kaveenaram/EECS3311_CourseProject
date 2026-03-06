from typing import List

from .booking import Booking

from .user import User
from .service import Service
from .timeslot import TimeSlot

"""
Consultant Class: Service provider who offers consulting sessions and manages availability
"""

class Consultant(User):

  # Consultant constructor initializes services, timeslots, bookings, and approval status, and uses User constructor for basic attributes
  def __init__(self, user_id: str, name: str, email: str, password: str):
        super().__init__(user_id, name, email, password)
        self.services: List[Service] = []
        self.timeslots: List[TimeSlot] = []
        self.bookings: List[Booking] = []
        self.approved: bool = False

  # Consultant login/logout methods with password check and approval status, and console messages
  # Overrides user login/logout to provide consultant-specific messages and functionality

  def logIn(self, password: str) -> bool:
        # if a consultant is not approved by an admin yet, they cannot log in
        if not self.approved:
            return False
        elif password == self.password:
            print(f"Welcome {self.name}")
            return True
        else:
            print(f"password incorrect. Please try again...")
            return False
        return super().logIn(password)
        
  def logOut(self) -> None:
        print(f"{self.name} logged out")

  # Consultant-specific methods for managing services, timeslots, and bookings

  def add_service(self, service: Service) -> None:
      self.services.append(service)

  def get_services(self) -> List[Service]:
      return self.services

  def add_timeslot(self, timeslot: TimeSlot) -> None:
      self.timeslots.append(timeslot)

  def get_available_timeslots(self) -> List[TimeSlot]:
      return [slot for slot in self.timeslots if slot.available]

  def get_bookings(self) -> List[Booking]:
      return self.bookings
  
  def __str__(self):
      return f"Consultant {self.name} | Email: {self.email} | Approved: {self.approved}"
