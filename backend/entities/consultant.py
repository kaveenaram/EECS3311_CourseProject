from typing import List
from .user import User
from .service import Service
from .timeslot import TimeSlot

class Consultant(User):

  def __init__(self, user_id: str, name: str, email: str):
      super().__init__(user_id, name, email)
      self.services: List[Service] = []
      self.timeslots: List[TimeSlot] = []

  def add_service(self, service: Service) -> None:
      self.services.append(service)

  def get_services(self) -> List[Service]:
      return self.services

  def add_timeslot(self, timeslot: TimeSlot) -> None:
      self.timeslots.append(timeslot)

  def get_available_timeslots(self) -> List[TimeSlot]:
      return [slot for slot in self.timeslots if slot.available]
