from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

"""
TimeSlot Class: Represents a specific time slot for a consulting session, including start and end times and availability status.
Consultants can create and manage their time slots, and clients can view available time slots
"""

class TimeSlot(Base):
    __tablename__ = "timeslots"

    slot_id = Column(String, primary_key=True)
    consultant_id = Column(String, ForeignKey('consultants.user_id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    available = Column(Boolean, default=True)
    
    consultant = relationship("Consultant", back_populates="timeslots")
    bookings = relationship("Booking", back_populates="timeslot")

  # TimeSlot constructor initializes slot ID, start time, end time, and availability status
    def __init__(self, slot_id: str, start_time: str, end_time: str):
      self.slot_id = slot_id
      self.start_time = start_time
      self.end_time = end_time
      self.available = True

  # Methods to mark time slot as available or unavailable, which can be called when a booking is made or canceled to update the slot's status
    def mark_unavailable(self):
      self.available = False


    def mark_available(self):
      self.available = True

    def __str__(self):
      return f"{self.start_time} - {self.end_time} | Available: {self.available}"
