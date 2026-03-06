from typing import List

from .booking import Booking

from .user import User
from .service import Service
from .timeslot import TimeSlot

class Consultant(User):

  def __init__(self, user_id: str, name: str, email: str, password: str):
        super().__init__(user_id, name, email, password)
        self.services: List[Service] = []
        self.timeslots: List[TimeSlot] = []
        self.bookings: List[Booking] = []
        self.approved: bool = False

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
