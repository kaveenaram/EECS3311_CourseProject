import uuid 
from datetime import datetime

"""
PaymentResult Class: Represents the outcome of a payment transaction, including success status, amount, timestamp, and a unique transaction ID.
"""

class PaymentResult:
  
  # PaymentResult constructor initializes transaction ID, success status, timestamp, and amount
  
  def __init__(self, success:bool, amount:float, timestamp: datetime):
    self.transactionID = str(uuid.uuid4()) # to Auto generate Transaction ID
    self.success = success
    self.timestamp = timestamp
    self.amount = amount

  def __str__(self):
    return(
      f"Transaction ID: {self.transactionID} \n"
      f"Success: {self.success} \n"
      f"Timestamp: {self.timestamp} \n"
      f"Amount: {self.amount}")

    
