from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .consultant import Consultant
from database.db import Base

"""
Service Class: Represents a consulting service offered by a consultant, including details like name, duration, price, and associated consultant.
"""

class Service(Base):
    __tablename__ = "services"

    service_id = Column(String(255), primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))
    duration = Column(Integer)  # duration in minutes
    price = Column(Float)
    consultant_id = Column(String(255), ForeignKey('consultants.user_id'))

    consultant = relationship("Consultant", back_populates="services")
    bookings = relationship("Booking", back_populates="service")

    # Service constructor initializes service attributes including a reference to the consultant offering the service

    def __init__(self, service_id: str, serviceName: str, duration: int, price: float, consultant: Consultant):
        self.service_id = service_id
        self.serviceName = serviceName
        self.duration = duration
        self.price = price
        self.consultant = consultant

    def __str__(self):
        return f"{self.serviceName} | {self.duration} mins | ${self.price}"
