import uuid 
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

"""
PaymentResult Class: Represents the outcome of a payment transaction, including success status, amount, timestamp, and a unique transaction ID.
"""

class PaymentResult(Base):
  __tablename__ = "payment_results"
  user_id = Column(String, primary_key=True)
  booking_id = Column(String, ForeignKey('bookings.booking_id'))
  success = Column(Boolean)
  amount = Column(Float)
  timestamp = Column(DateTime)

  booking = relationship("Booking", back_populates="payment_history")

  # PaymentResult constructor initializes transaction ID, success status, timestamp, and amount
  
  def __init__(self, success:bool, amount:float, timestamp: datetime):
    self.transactionID = str(uuid.uuid4()) # to Auto generate Transaction ID
    self.success = success
    self.timestamp = timestamp
    self.amount = amount

  def __str__(self):
    return (
      f"Transaction ID: {self.transactionID} \n"
      f"Success: {self.success} \n"
      f"Timestamp: {self.timestamp} \n"
      f"Amount: {self.amount}"
    )

    
