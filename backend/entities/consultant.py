from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .user import User
from backend.database import db

"""
Consultant Class: Service provider who offers consulting sessions and manages availability
"""

class Consultant(User):
    __tablename__ = "consultants"

    user_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    approved = Column(Boolean, default=False)
    services = relationship("Service", back_populates="consultant")
    timeslots = relationship("TimeSlot", back_populates="consultant")
    bookings = relationship("Booking", back_populates="consultant", foreign_keys='Booking.consultant_id')

    __mapper_args__ = {
        'polymorphic_identity': 'consultant'
    }

    # Consultant constructor initializes services, timeslots, bookings, and approval status, and uses User constructor for basic attributes
    def __init__(self, user_id: str, name: str, email: str, password: str):
        super().__init__(user_id, name, email, password)
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

    def add_service(self, service) -> None:
        self.services.append(service)

    def get_services(self):
        return self.services

    def add_timeslot(self, timeslot) -> None:
        self.timeslots.append(timeslot)

    def get_available_timeslots(self):
        from entities.timeslot import TimeSlot
        return db.query(TimeSlot).filter_by(
            consultant_id=self.user_id, available=True
            ).all()

    def get_bookings(self):
        return self.bookings
  
    def __str__(self):
        return f"Consultant {self.name} | Email: {self.email} | Approved: {self.approved}"
